import pandas
import numpy
import requests
from bs4 import BeautifulSoup

def read_xbrlxml(path = numpy.nan):

    # Pull the raw html code from the applicable website or file path
    if requests.get(path).status_code == 200:
        websitedocument = requests.get(path).content
        soup = BeautifulSoup(websitedocument, 'lxml-xml')
    else:
        try:
            soup = BeautifulSoup(open(path), 'lxml-xml')
        except Exception:
            print("Path Does Not Correspond to a Website or Valid File Path")
        pass

    # Pull a list of the descriptive columns to populate an empty dataframe
    tag_list = soup.select("context")
    columnlist = ["context"]
    for n in tag_list:
        for nholder in n.recursiveChildGenerator():
            if nholder.name != None and \
            nholder.name not in columnlist and \
                    r'"\"' not in nholder.name and \
                    nholder.name != "html" and \
                    nholder.name != "body" and \
                    nholder.name != "xbrl":
                columnlist.append(nholder.name)
    columnlist.append('datacode')
    columnlist.append('datavalue')
    print(columnlist)

    # Create an initialized dataframe to describe each unique context identifier
    outputframe = \
        pandas.DataFrame(
        columns=list(columnlist),
        dtype = 'object'
        )
    outputframe.datacode = ""
    outputframe.datavalue = ""

    # Populate the outputframe with all descriptive supplementary data to be populated later
    for tag in tag_list:
        # Create a dataframe row to explain the context identifier descriptive data
        insertframe = \
            pandas.DataFrame(
            columns=columnlist,
            data = numpy.full([1, columnlist.__len__(),], numpy.nan) )
        # Parse through each column name to extract the applicable data

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
                            insertframe[columnname] = tag.find(columnname).findChild().text
                        else:
                            insertframe[columnname] = numpy.nan

        # Append the new row of data to the existing data frame
        outputframe = outputframe.append(insertframe)

    # Create a modifiedsoup that only contains the datavalues & datacode. The data is identified by a contextRef tag that matches the context tag as identified above
    modifiedsoup = soup.findAll(attrs={"contextRef" : not None})

    for selectionchoice in modifiedsoup:
        # Specify the data values & pull the descriptive data
        uniqueidentifier = selectionchoice.get('contextRef')
        rawdataframe = outputframe[outputframe.context == uniqueidentifier].drop_duplicates(subset=['identifier'])
        titleholder = str(selectionchoice.name)
        outputvalueholder = str(selectionchoice.text)

        # If data does not exist in the dataset, update the existing null dataset.
        if str(rawdataframe.iloc[0]['datavalue']) == 'nan' and str(rawdataframe.iloc[0]['datacode']) == 'nan':
            # Parse through all keys & add as their own column
            for keyholder in list(selectionchoice.attrs.keys()) :
                # Avoid contextRef & id as it is redundant to context. Values with : are unnecessary
                if keyholder != 'contextRef' and keyholder != 'id':
                    outputframe.loc[outputframe.context == uniqueidentifier, keyholder] = selectionchoice.get(keyholder)
            outputframe.loc[outputframe.context == uniqueidentifier, 'datacode'] = titleholder
            outputframe.loc[outputframe.context == uniqueidentifier, 'datavalue'] = outputvalueholder

        # If not the first iteration, add a new row.
        else:
            # Use the raw dataframre to initialize the new row, then modify
            insertvalue = rawdataframe
            # Parse through all keys & add as their own column
            for keyholder in list(selectionchoice.attrs.keys()) :
                # Avoid contextRef & id as it is redundant to context. Values with : are unnecessary
                if keyholder != 'contextRef' and keyholder != 'id':
                    insertvalue.loc[0, keyholder] = selectionchoice.get(keyholder)
            # insert the new value to the dataframe
            insertvalue.datacode = titleholder
            insertvalue.datavalue = outputvalueholder
            outputframe = outputframe.append(insertvalue)

    #convert empty strings to NULL, & remove all columns with only NULL or blank values
    outputframe = outputframe
    outputframe = outputframe.replace('', numpy.nan)
    outputframeclean = outputframe.dropna(axis=1, how='all')

    # Reorder the columns to present the datacode & datavalue at the right most column
    columnsTitles = list(outputframeclean.columns)
    columnsTitles.remove('datacode')
    columnsTitles.remove('datavalue')
    columnsTitles.append('datacode')
    columnsTitles.append('datavalue')
    outputframeclean = outputframeclean.reindex(columns=columnsTitles)

    return outputframeclean.sort_values(by=['context'])

