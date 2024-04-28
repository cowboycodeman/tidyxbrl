import pandas
import requests
import numpy


def edgar_cik():
    """
    The edgar_cik function is used to pull Central Index Key (CIK) for reporting companies 
    Inputs:

    Outputs:
        companies: Return a pandas DataFrame of reporting companies and their associated CIK. Note that the CIK is converted to 10 digits with leading 0s

    Examples:
        - edgar_cik()
    """

    # Read the company JSON from the SEC
    url = "https://www.sec.gov/files/company_tickers.json"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',  # Do Not Track Request Header
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    data = requests.get(url, headers=headers)
    
    companies = pd.DataFrame(data.json()).transpose()

    # Convert each company CIK into a 10 digit CIK for the API
    columnoverride = []
    for shortcik in companies.cik_str:
        valappender = 10 - str(shortcik).__len__()
        valueout = ''.join(str(a)
                           for a in numpy.repeat(0, valappender)) + str(shortcik)
        columnoverride.append(valueout)

    # Override the column with the 10-digit CIK values
    companies.cik_str = columnoverride
    return companies
