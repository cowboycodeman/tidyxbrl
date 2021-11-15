import pandas
import requests
import numpy
from tqdm import tqdm

def edgar_query(companycik, query_type, queryextension = ''):
    """
    https://www.sec.gov/edgar/sec-api-documentation
    The edgar_query function is used to query SEC data using the CIK determined in edgar_companycik  
    Inputs:
        companycik: Unique company CIK value pulled in edgar_companycik. Note that the CIK is converted to 10 digits with leading 0s
        query_type: The type of API query:
            - submissions: Each entity’s current filing history
            - companyconcept: The company-concept API returns all the XBRL disclosures from a single company (CIK) and concept (a taxonomy and tag) into a single JSON file, with a separate array of facts for each units on measure that the company has chosen to disclose
            - companyfacts: This API returns all the company concepts data for a company into a single API call
        queryextension: Extension required for companyconcept query types to specify the desired report type

    Outputs:
        longdata: Tidy dataframe housing the report data

    Examples:
        - edgar_query('0000789019', query_type = 'submissions')
        - edgar_query('0000789019', query_type = 'companyconcept', queryextension = '/us-gaap/AccountsPayableCurrent.json')
        - edgar_query('0000789019', query_type = 'companyfacts')
    """
    
    
    querydict = {'submissions': 'https://data.sec.gov/submissions/CIK', 
    'companyconcept': 'https://data.sec.gov/api/xbrl/companyconcept/CIK', 
    'companyfacts': 'https://data.sec.gov/api/xbrl/companyfacts/CIK'}
    
    if query_type not in querydict.keys():
        raise ValueError("parse_type must be in: " + str(querydict.keys()))
    
    urlquery = querydict[query_type]
    dataquery = urlquery + companycik + str(queryextension).replace(".json", "") + ".json"
    soupheaders = {'User-Agent': 'Mozilla'}
    dataresponse = requests.get(url=dataquery, headers = soupheaders)
    result = pandas.DataFrame(pandas.json_normalize(dataresponse.json()))
    longdata = pandas.melt(result, id_vars = ['cik'])
    
    for valueholder in tqdm(range(1,longdata.value.__len__())):
        loadvalue = longdata.iloc[valueholder].value
        if(str(type(loadvalue)) == "<class 'list'>" and loadvalue.__len__() > 1):
            try: 
                longdata.at[valueholder, 'value'] = (pandas.json_normalize(loadvalue))
            except:
                pass
    
    return longdata

def edgar_frames(urldescriptor = ''):
    """
    The edgar_frames function aggregates one fact for each reporting entity that is last filed that most closely fits the calendrical period requested. This API supports for annual, quarterly and instantaneous data
    
    Inputs:
        urldescriptor: URL description of the frame query (everything after https://data.sec.gov/api/xbrl/frames/). The data is structured as:
        finstandard/reporttype/denomination/dateholder 
            - finstandard: The financial reporting standard
                * us-gaap 
                * ifrs-full
                * dei
                * srt
            - reporttype: The type of report to query. See the datacode in the xbrl_parse function using 'xml' parse_type (i.e. NonoperatingIncomeExpense)
            - denomination: Report currency (i.e. USD)
            - dateholder: Date of evaluation (i.e. CY2019Q1I)
    
    Outputs:
        return companies: Return a pandas DataFrame of reporting companies and their associated CIK
    
    Examples:
        - edgar_frames(urldescriptor = 'us-gaap/NonoperatingIncomeExpense/USD/CY2019Q1I.json')
    """
    
    
    dataquery = 'https://data.sec.gov/api/xbrl/frames/' + urldescriptor
    soupheaders = {'User-Agent': 'Mozilla'}
    dataresponse = requests.get(url=dataquery, headers = soupheaders)
    result = pandas.DataFrame(pandas.json_normalize(dataresponse.json()))
    longdata = pandas.melt(result, id_vars = ['taxonomy'])
    
    for valueholder in tqdm(range(1,longdata.value.__len__())):
        loadvalue = longdata.iloc[valueholder].value
        if(str(type(loadvalue)) == "<class 'list'>" and loadvalue.__len__() > 1):
            try: 
                longdata.at[valueholder, 'value'] = (pandas.json_normalize(loadvalue))
            except:
                pass
    
    
    return longdata
