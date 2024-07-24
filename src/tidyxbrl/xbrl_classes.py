"""

"""
# %%
import pandas
import numpy
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm



# %%

class DataRequest:
    def __init__(self, xbrl):
        self.xbrl = xbrl
        self.data = self.get_data()

class XBRL:
    def __init__(self, xbrl_file):
        self.xbrl_file = xbrl_file
        self.xbrl = self.load_xbrl()
        self.xbrl_dict = self.xbrl_to_dict()
    
    def xbrl_parse(self, 
                   path, 
                   timeout_sec=15
                   ):
        """
        The xbrl_apikey function is used to parse the metadata from a particular XBRL file or
        website url.

        Args:
            path (str): Filepath or website url corresponding to XBRL data.
            timeout_sec: The time in seconds to wait for the server to respond

        Returns:
            pandas.DataFrame: DataFrame output of the XBRL file in a tidy format.
                Descriptive Columns: Dynamic columns that describe the dataset. The columns below
                outline the SEC file format, and are due to change based on the data source.
                    - context: Unique identity assigned to all item facts.
                    - identifier: The value of the scheme attribute of the entity identifier.
                    - startdate: Beginning date of the dataset (applies to duration time periods).
                    - enddate: Ending date of the dataset (applies to duration time periods).
                    - segment: Tag that allows additional information to be included in the context
                    of an instance document.
                    - instant: Instant date of the data set. Captures an instance in time.
                    - decimals: Number of decimals in the dataset.
                    - unitref: Unit of the dataset.
                Data Columns:
                    - datacode: Description of the dataset.
                    - datvalue: Value of the dataset.

        Examples:
            xbrl_parse('https://www.sec.gov/Archives/edgar/data/320193/000032019321000010/aapl-20201226_htm.xml')
            xbrl_parse('https://www.sec.gov/Archives/edgar/data/51143/000155837020001334/ibm-20191231x10k2af531_htm.xml')
            xbrl_parse('https://www.sec.gov/Archives/edgar/data/1318605/000156459020047486/tsla-10q_20200930_htm.xml')
        """

        def xbrlcolumnprefilter(tag):
            return (
                tag.name != "body"
                and tag.name != "xbrl"
                and tag.name != "html"
                and tag.prefix == ""
                and ":" not in tag.name
            )

        soupheaders = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "DNT": "1",  # Do Not Track Request Header
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
        initialrequest = requests.get(path, headers=soupheaders, timeout=timeout_sec)
        if initialrequest.status_code == 200:
            websitedocument = initialrequest.content
            soup = BeautifulSoup(websitedocument, "xml")
        else:
            try:
                with open(path, "r", encoding="utf-8") as file:
                    soup = BeautifulSoup(file, "xml")
            except ValueError:
                print("Path Does Not Correspond to a Website or Valid File Path")

        # Pull a list of the descriptive columns to populate an empty dataframe
        tag_listall = soup.find_all(xbrlcolumnprefilter)
        empty_tag_list = soup.select("context")
        columnlist = []
        for temp_tag in tag_listall:
            if temp_tag.name not in list(numpy.unique(columnlist)):
                columnlist.append(temp_tag.name)

        columnlist = list(columnlist) + ["datacode", "datavalue"]
        print(columnlist)

        data = []
        for tag in tqdm(empty_tag_list, desc="Processing Unique Identifiers"):
            row = {}
            for columnname in columnlist:
                if columnname == "context":
                    row[columnname] = tag.get("id")
                else:
                    if tag.find(columnname):
                        if not tag.find(columnname).findChild():
                            row[columnname] = tag.find(columnname).text
                        elif tag.find(columnname).findChild().name not in columnlist:
                            row[columnname] = tag.find(columnname).findChild().text
                        else:
                            row[columnname] = numpy.nan
            data.append(row)

        outputframe = pandas.DataFrame(data, columns=columnlist)

        data_for_tag_list = soup.findAll(attrs={"contextRef": not None})

        data = []
        for selectionchoice in tqdm(data_for_tag_list, desc="Processing Data Points"):
            uniqueidentifier = selectionchoice.get("contextRef")
            rawdataframe = outputframe[outputframe.context == uniqueidentifier].drop_duplicates(subset=["identifier"])
            titleholder = str(selectionchoice.name)
            outputvalueholder = str(selectionchoice.text)

            row = rawdataframe.iloc[0].to_dict()
            if pandas.isnull(row["datavalue"]) and pandas.isnull(row["datacode"]):
                for keyholder in selectionchoice.attrs.keys():
                    if keyholder not in ["contextRef", "id"] and ":" not in keyholder:
                        row[keyholder] = selectionchoice.get(keyholder)
                row["datacode"] = titleholder
                row["datavalue"] = outputvalueholder
            else:
                filteredselection = [
                    k
                    for k in selectionchoice.attrs.keys()
                    if k not in ["contextRef", "id"] and ":" not in k
                ]
                for keyholder in filteredselection:
                    row[keyholder] = selectionchoice.get(keyholder)
                row["datacode"] = titleholder
                row["datavalue"] = outputvalueholder
            data.append(row)

        outputframe = pandas.DataFrame(data)

        # convert empty strings to NULL, & remove all columns with only NULL or blank values
        outputframe = outputframe.replace("", numpy.nan).dropna(axis=1, how="all")

        # Reorder the columns to present the datacode & datavalue at the rightmost column
        columnstitles = list(outputframe.columns)
        columnstitles.sort(key=lambda x: x == "datacode")
        columnstitles.sort(key=lambda x: x == "datavalue")
        outputframe = outputframe.reindex(columns=columnstitles)

        return outputframe.sort_values(by=["context"])
    
    def xbrl_query(
        self,
        access_token,
        queryparameters,
        baseapiurl="https://api.xbrl.us/api/v1/report/search?",
        timeout_sec = 15
    ):
        """
        https://xbrl.us/home/use/xbrl-api/
        http://files.xbrl.us/documents/XBRL-API-V1.4.pdf

        The xbrl_query function is used to query the xbrl api using the token generated in the
        xbrl_apikey function.

        Args:
            access_token: Access token string generated in the xbrl_apikey function. Found in the
            access_token column of the response dataframe.
            baseapiurl: API request URL corresponding to the type of request prior to passing any
            parameters. This is everything up-to and including the "?" in the API request
                - 'https://api.xbrl.us/api/v1/report/search?'
                - 'https://api.xbrl.us/api/v1/fact/search?'
            queryparameters: Dictionary structure to specify each aspect of the api request (See the
            Examples section below)

        Outputs:
            xbrl_queryoutput: Pandas Dataframe object corresponding to the fields specified in the
            request

        Examples:
            - xbrl_query(access_token=xbrl_apikeyoutput.access_token.values[0],
                        baseapiurl='https://api.xbrl.us/api/v1/report/search?',
                        queryparameters = {'report.entity-name': "APPLE INC.",
                                            'fields': "report.id,report.entity-name,report.filing-date,
                                            report.base-taxonomy,report.document-type,report.accession,
                                            entity.ticker,report.sic-code,entity.cik,report.entry-type,
                                            report.period-end,report.sec-url,report.checks-run,
        """

        # Modify the queryparameter keys to create a web request string in dataquery
        # Add the "=" sign between keys and values
        for keyholder in list(queryparameters.keys()):
            queryparameters[keyholder + "="] = queryparameters[keyholder]
            del queryparameters[keyholder]
        # Add the "&" sign between keys
        queryurl = "".join(
            [f"{key}{value}&" for key, value in queryparameters.items()]
        )[:-1]
        # Add the baseurl and modified request values
        dataquery = str(baseapiurl + queryurl)
        # Generate the authentication bearer tolken
        headers = {"Authorization": "Bearer " + access_token}
        # Generate the response
        dataresponse = requests.get(url=dataquery, headers=headers, timeout=timeout_sec)
        # Check the Response Code
        if dataresponse.status_code == 200:
            try:
                xbrl_queryoutput = pandas.DataFrame.from_dict(dataresponse.json()["data"])
            except Exception as exc:
                raise ValueError(str(dataresponse.json())) from exc
        else:
            xbrl_queryoutput = dataresponse.status_code
            print(dataresponse.text)
            raise ValueError(str(xbrl_queryoutput) + ": Error in Response")
        return xbrl_queryoutput

    

            