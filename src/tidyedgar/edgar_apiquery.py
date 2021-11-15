import pandas
import requests
import numpy
from tqdm import tqdm

companyclk = "0000789019"
year = "2019"
datevalue = "Q1"
category = "NonoperatingIncomeExpense"
unit = "USD"

def edgar_tickerquery():
    companies = pandas.read_json("https://www.sec.gov/files/company_tickers.json", orient = "index")
    columnoverride = []
    for shortcik in companies.cik_str:
        valappender = 10 - str(shortcik).__len__()
        valueout = ''.join(str(a) for a in numpy.repeat(0,valappender)) + str(shortcik)
        columnoverride.append(valueout)
    
    companies.cik_str = columnoverride
    return companies

def edgar_submissions(companyclk = ''):
    
    dataquery = "https://data.sec.gov/submissions/CIK" + companyclk + ".json"
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

def edgar_companyconcept(companyclk = ''):
    
    dataquery = "https://data.sec.gov/api/xbrl/companyconcept/CIK" + companyclk + "/us-gaap/AccountsPayableCurrent.json"
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

def edgar_companyfacts(companyclk = ''):
    
    dataquery = "https://data.sec.gov/api/xbrl/companyfacts/CIK" + companyclk + ".json"
    soupheaders = {'User-Agent': 'Mozilla'}
    dataresponse = requests.get(url=dataquery, headers = soupheaders)
    result = pandas.DataFrame(pandas.json_normalize(dataresponse.json()))
    longdata = pandas.melt(result, id_vars = ['cik'])
    longdata.value.astype
    
    for valueholder in tqdm(range(1,longdata.value.__len__())):
        loadvalue = longdata.iloc[valueholder].value
        if(str(type(loadvalue)) == "<class 'list'>" and loadvalue.__len__() > 1):
            try: 
                longdata.at[valueholder, 'value'] = (pandas.json_normalize(loadvalue))
            except:
                pass
    
    return longdata

def edgar_frames(year = '', datevalue = '', category = '', unit = ''):
    
    dataquery = 'https://data.sec.gov/api/xbrl/frames/us-gaap/' + category + '/' + unit + '/' + 'CY' + year + datevalue + 'I.json'
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


