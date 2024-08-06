"""
Function to parse raw XBRL files from a website or file path.
"""

import pandas
import numpy
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from src.config.default_headers import con_headers_default


def xbrl_parse(path, timeout_sec=15, con_headers = con_headers_default):
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

    initialrequest = requests.get(path, headers=con_headers, timeout=timeout_sec)
    if initialrequest.status_code == 200:
        websitedocument = initialrequest.content
        soup = BeautifulSoup(websitedocument, "xml")
    else:
        try:
            with open(path, "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file, "xml")
        except (OSError, ValueError, requests.RequestException) as e:
            print(f"Error: {e}")
            return None

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
