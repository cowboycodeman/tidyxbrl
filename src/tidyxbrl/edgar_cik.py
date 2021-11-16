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
    companies = pandas.read_json(
        "https://www.sec.gov/files/company_tickers.json", orient="index")
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
