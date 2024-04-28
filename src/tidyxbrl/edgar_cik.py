"""
The Central Index Key (CIK) is a unique identifier assigned by 
the U.S. Securities and Exchange Commission (SEC) to reporting companies. 
It is used to track and identify these companies in various SEC filings and databases. 
The CIK is a 10-digit number, and this function converts the CIKs of reporting companies 
into 10-digit format with leading zeros.
"""

import pandas
import requests
import numpy


def edgar_cik(timeout_sec = 15):
    """
    The edgar_cik function is used to pull Central Index Key (CIK) for reporting companies
    
    Args:
        timeout_sec: The time in seconds to wait for the server to respond

    Outputs:
        companies: Pandas DataFrame of companies and their CIKconverted to 10 digits with leading 0s

    Examples:
        - edgar_cik()
    """

    # Read the company JSON from the SEC
    url = "https://www.sec.gov/files/company_tickers.json"
    headers = {
        "User-Agent": "Mozilla",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "DNT": "1",  # Do Not Track Request Header
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    data = requests.get(url, headers=headers, timeout=timeout_sec)

    companies = pandas.DataFrame(data.json()).transpose()

    # Convert each company CIK into a 10 digit CIK for the API
    columnoverride = []
    for shortcik in companies.cik_str:
        valappender = 10 - len(str(shortcik))
        valueout = "".join(str(a) for a in numpy.repeat(0, valappender)) + str(shortcik)
        columnoverride.append(valueout)

    # Override the column with the 10-digit CIK values
    companies.cik_str = columnoverride
    return companies
