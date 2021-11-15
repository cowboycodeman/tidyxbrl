import pandas
import requests
import numpy
from tqdm import tqdm

def edgar_queryframes(urldescriptor = ''):
    """
    The edgar_apiqueryframes function aggregates one fact for each reporting entity that is last filed that most closely fits the calendrical period requested. This API supports for annual, quarterly and instantaneous data
    
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
        - edgar_queryframes(urldescriptor = 'us-gaap/NonoperatingIncomeExpense/USD/CY2019Q1I.json')
    """
    
    
    dataquery = 'https://data.sec.gov/api/xbrl/frames/' + str(urldescriptor).replace(".json", "") + ".json"
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