"""
The Central Index Key (CIK) is a unique identifier assigned by
the U.S. Securities and Exchange Commission (SEC) to reporting companies.
It is used to track and identify these companies in various SEC filings and databases.
The CIK is a 10-digit number, and this function converts the CIKs of reporting companies
into 10-digit format with leading zeros.
"""

# https://www.sec.gov/edgar/searchedgar/companysearch
# https://www.edgarcompany.sec.gov/servlet/CompanyDBSearch?page=main

import re
import httpx
from bs4 import element
from bs4 import BeautifulSoup
import pandas as pd
from src.config.default_headers import con_headers_default

# %%


def edgar_cik(
    query,
    comprehensive=False,
    start_row=0,
    timeout_sec=15,
    last_company_df=pd.DataFrame(),
    max_start_row=25000,
    con_headers = con_headers_default
):
    """
    The edgar_cik function is used to pull Central Index Key (CIK) for reporting companies

    Args:
        query: The company name or ticker symbol to search for
        comprehensive: Whether to retrieve all available results or just the first 100
        start_row: The starting index for retrieving results
        timeout_sec: The time in seconds to wait for the server to respond
        last_company_df: (comprehensive = True) The previous DataFrame to compare with current
        max_start_row: The maximum starting index for retrieving results
        con_headers (dict): The headers to be sent with the initial request.

    Returns:
        company_df: Pandas DataFrame of company names, CIK, and state

    Examples:
        -  edgar_cik(
            query = 'App',
            comprehensive=True,     
            start_row=0,
            timeout_sec=15,
            last_company_df=pd.DataFrame(),
            max_start_row=25000,)
    """

    # Read the company JSON from the SEC

    url = "https://www.sec.gov/cgi-bin/browse-edgar"  # Replace with your desired CIK

    payload = {
        "company": query,
        "match": "starts-with",
        "count": 100,
        "start": start_row,
    }

    response = httpx.post(url, headers=con_headers, data=payload, timeout=timeout_sec)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the table in the HTML
    table = soup.find("table", {"class": "tableFile2"})

    if soup.find(class_='companyName') is not None:
        company_names = str(soup.find(class_='companyName').text).split('CIK#: ', maxsplit=1)[0]
        cik_codes = str(re
                          .findall("\d+",
                                   str(soup.find(class_="companyName").text)
                                   .split("CIK#: ")[1]
                                   .strip())[0])
        states = (
            soup.find(class_="identInfo")
            .text.split("State location: ")[1]
            .split("|")[0]
            .strip()
        )
        company_df = pd.DataFrame(
            {
                "cik": pd.to_numeric(cik_codes),
                "cik_str": [cik_codes],
                "company": [company_names],
                "state": [states],
            }
        )
        return company_df

    # Extract the table rows
    if isinstance(table, element.Tag):
        rows = table.find_all("tr")

        # Extract the CIK Codes, Company Names and States
        cik_codes = []
        company_names = []
        states = []
        for row in rows[1:]:  # Ignore the header row
            cols = row.find_all("td")
            cik_code = cols[0].text
            company_name = cols[1].text
            state = cols[2].text
            cik_codes.append(cik_code)
            company_names.append(company_name)
            states.append(state)

        # Create a pandas DataFrame
        company_df = pd.DataFrame(
            {"cik": pd.to_numeric(cik_codes), "cik_str": cik_codes ,"company": company_names, "state": states}
        )
        print(f"Start Row: {start_row} - {company_df.iloc[0]['company']}")

        if (
            (comprehensive is True)
            & (len(company_df) == 100)
            & (last_company_df.equals(company_df) is False)
            & (start_row < max_start_row)
        ):
            new_company_df = edgar_cik(
                query,
                comprehensive=comprehensive,
                start_row=start_row + 100,
                last_company_df=company_df,
            )

            company_df = pd.concat([company_df, new_company_df]).reset_index(drop=True)

        return company_df

    print(f"Final Row Reached At {start_row}")
    return pd.DataFrame()

# %%
