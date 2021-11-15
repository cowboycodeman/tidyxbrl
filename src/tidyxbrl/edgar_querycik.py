import pandas
import requests
import numpy

def edgar_querycik():
    """
    The edgar_querycik function is used to pull Central Index Key (CIK) for reporting companies for later queries 
    Inputs:

    Outputs:
        companies: Return a pandas DataFrame of reporting companies and their associated CIK. Note that the CIK is converted to 10 digits with leading 0s

    Examples:
        - edgar_querycik()
    """
    
    
    companies = pandas.read_json("https://www.sec.gov/files/company_tickers.json", orient = "index")
    columnoverride = []
    for shortcik in companies.cik_str:
        valappender = 10 - str(shortcik).__len__()
        valueout = ''.join(str(a) for a in numpy.repeat(0,valappender)) + str(shortcik)
        columnoverride.append(valueout)
    
    companies.cik_str = columnoverride
    return companies