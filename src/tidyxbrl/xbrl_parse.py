import pandas
import numpy
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# Function to parse xbrl files or website urls
def xbrl_parse(path=''):
    """
    The xbrl_apikey function is used to parse the metadata from a particular XBRL file.  
    Inputs:
        path: filepath or website url corresponding to XBRL data

    Outputs:
        xbrl_parseoutput: Pandas DataFrame output of the XBRL file in a tidy format
            Descriptive Columns: Dynamic Columns that describe the dataset. The columns below outline the SEC file format, and are due to change based on the data source.
                - context: Unique identity assigned to all item facts
                - identifier: The value of the scheme attribute of the identifier of the entity
                - startdate: Beginning date of the dataset (This applies to duration time periods)
                - enddate: Ending date of the dataset (This applies to duration time periods)
                - segment: Tag that allows additional information to be included in the context of an instance document; this information captures segment information such as an entity's business units, type of debt, type of other income, and so forth.
                - instant: Instant date of the data set. This caputures an instance in time, and cannot co-exist with he startdate & enddate parameters 
                - decimals: Number of decimals in the dataset
                - unitref: Unit of the dataset
            Data Columns:
                - datacode: Description of the dataset
                - datvalue: Value of the dataset

    Examples:
        - xbrl_parse('https://www.sec.gov/Archives/edgar/data/320193/000032019321000010/aapl-20201226_htm.xml')
        - xbrl_parse('https://www.sec.gov/Archives/edgar/data/51143/000155837020001334/ibm-20191231x10k2af531_htm.xml')
        - xbrl_parse('https://www.sec.gov/Archives/edgar/data/1318605/000156459020047486/tsla-10q_20200930_htm.xml')
    """
    
    
    # Specify Inner Functions
    # Pass the table through a filter to remove all unnecessary tags (body, html, :) that don't describe descriptive columns
    def xbrlcolumnprefilter(tag):
        return tag.name != 'body' and tag.name != 'xbrl' and tag.name != 'html' and ":" not in tag.name

    soupheaders = {'User-Agent': 'Mozilla'}
    initialrequest = requests.get(path, headers=soupheaders)
    # Pull the raw html code from the applicable website or file path
    if initialrequest.status_code == 200:
        websitedocument = initialrequest.content
        soup = BeautifulSoup(websitedocument, 'lxml')
    else:
        try:
            soup = BeautifulSoup(open(path), 'lxml')
        except Exception:
            print("Path Does Not Correspond to a Website or Valid File Path")
        pass
    
    # Pull a list of the descriptive columns to populate an empty dataframe with the filter function defined above
    tag_listall = soup.find_all(xbrlcolumnprefilter)
    tag_list = soup.select("context")
    columnlist = []
    for n in tag_listall:
        if n.name not in columnlist:
            columnlist.append(n.name)
    
    # Append datacode (unique identifier) and datavalue (unique value) to be populated in later steps
    columnlist.append('datacode')
    columnlist.append('datavalue')
    print(columnlist)
    # Create an initialized dataframe to describe each unique context identifier that corresponds to a datacode/datavalue set
    outputframe = \
        pandas.DataFrame(
            columns=list(columnlist),
            dtype='object'
        )
    outputframe.datacode = ""
    outputframe.datavalue = ""
    # Populate the outputframe with all descriptive supplementary data to be populated in laer steps
    # This steps defines the number of unique context reference codes and sets the descriptive values
    # There can be multiple values per context reference codes, which will be populated in later steps in a tidy format
    for tag in tqdm(tag_list):
        # Create a dataframe row to explain the  descriptive data for each context identifier
        insertframe = \
            pandas.DataFrame(
                columns=columnlist,
                data=numpy.full([1, columnlist.__len__(), ], numpy.nan))
        # Parse through each column name to extract the applicable column data
        for columnname in columnlist:
            # Context contains the unique description identifier
            if columnname == 'context':
                insertframe[columnname] = tag.get('id')
            else:
                # If there are child nodes, then discard. Only Pull the lowest level of data housing the values
                if not not tag.find(columnname):
                    if not tag.find(columnname).findChild():
                        insertframe[columnname] = tag.find(columnname).text
                    elif tag.find(columnname).findChild().name not in columnlist:
                        insertframe[columnname] = tag.find(
                            columnname).findChild().text
                    else:
                        insertframe[columnname] = numpy.nan
        
        # Append the new row of data to the existing data frame
        outputframe = outputframe.append(insertframe)
    
    # Contextref corresponds to the values that actually store the unique datacode/datavalue sets
    # Create a modifiedsoup that only contains the datavalues & datacode. The data is identified by a contextref tag that matches the context tag in the outputframe above
    # This step populates the outputframe and adds new rows for duplicated datasets
    modifiedsoup = soup.findAll(attrs={"contextref": not None})
    outputframebasic = outputframe #Does not expand. Lowers computation for large datasets
    for selectionchoice in tqdm(modifiedsoup):
        # Specify the data values & pull the descriptive data
        uniqueidentifier = selectionchoice.get('contextref')
        rawdataframe = outputframe[outputframe.context == uniqueidentifier].drop_duplicates(
            subset=['identifier'])
        titleholder = str(selectionchoice.name)
        outputvalueholder = str(selectionchoice.text)
        # If data does not exist in the existing dataset, update the existing null dataset else create a new row.
        # The if statement checks if the existing data contains data.
        if str(rawdataframe.iloc[0]['datavalue']) == 'nan' and str(rawdataframe.iloc[0]['datacode']) == 'nan':
            # Parse through all columns specified by keyholder populate each column
            for keyholder in list(selectionchoice.attrs.keys()):
                # Avoid contextref & id as it is a duplicate to context. Values with ':' are unnecessary
                if keyholder != 'contextref' and keyholder != 'id' and ":" not in keyholder:
                    outputframe.loc[outputframe.context == uniqueidentifier, keyholder] = selectionchoice.get(keyholder)
            outputframe.loc[outputframe.context == uniqueidentifier, 'datacode'] = titleholder
            outputframe.loc[outputframe.context == uniqueidentifier, 'datavalue'] = outputvalueholder
        # If not the first iteration, add a new row.
        else:
            # Use the raw dataframe to initialize the new row, then modify. Remove duplicate id and contextref columns
            filteredselection = list(selectionchoice.attrs.keys())
            filteredselection.remove('contextref')
            filteredselection.remove('id')  
            for keyholder in filteredselection:
                # Parse through all keys & add as their own column
                if ":" not in keyholder:
                    rawdataframe.loc[0, keyholder] = selectionchoice.get(
                        keyholder)
            # insert the new value to the dataframe
            rawdataframe.datacode = titleholder
            rawdataframe.datavalue = outputvalueholder
            outputframe = outputframe.append(rawdataframe)
    
    # convert empty strings to NULL, & remove all columns with only NULL or blank values
    outputframe = outputframe.replace('', numpy.nan)
    xbrl_parseoutput = outputframe.dropna(axis=1, how='all')
    # Reorder the columns to present the datacode & datavalue at the right most column
    columnsTitles = list(xbrl_parseoutput.columns)
    columnsTitles.sort(key = 'datacode'.__eq__)
    columnsTitles.sort(key = 'datavalue'.__eq__)
    xbrl_parseoutput = xbrl_parseoutput.reindex(columns=columnsTitles)
    return xbrl_parseoutput.sort_values(by=['context'])