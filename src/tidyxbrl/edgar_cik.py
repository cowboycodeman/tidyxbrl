"""
The Central Index Key (CIK) is a unique identifier assigned by 
the U.S. Securities and Exchange Commission (SEC) to reporting companies. 
It is used to track and identify these companies in various SEC filings and databases. 
The CIK is a 10-digit number, and this function converts the CIKs of reporting companies 
into 10-digit format with leading zeros.
"""

# https://www.sec.gov/edgar/searchedgar/companysearch
# https://www.edgarcompany.sec.gov/servlet/CompanyDBSearch?page=main


import requests
from bs4 import element
from bs4 import BeautifulSoup
import pandas as pd

# %%

def edgar_cik(query, comprehensive = False, start_row = 0, timeout_sec = 15, last_df = pd.DataFrame(), max_start_row = 25000):
    """
    The edgar_cik function is used to pull Central Index Key (CIK) for reporting companies
    
    Args:
        query: The company name or ticker symbol to search for
        comprehensive: Whether to retrieve all available results or just the first 100
        start_row: The starting index for retrieving results
        timeout_sec: The time in seconds to wait for the server to respond

    Outputs:
        df: Pandas DataFrame of companies and their CIK converted to 10 digits with leading 0s

    Examples:
        - edgar_cik('Apple Inc.', comprehensive=True)
    """

    # Read the company JSON from the SEC
    headers = {
        "User-Agent": "Mozilla",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "DNT": "1",  # Do Not Track Request Header
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    url = 'https://www.sec.gov/cgi-bin/browse-edgar'  # Replace with your desired CIK

    payload = {"company": query,
            "match":"starts-with",
            "count": 100,
            "start": start_row
            }

    response = requests.post(url, headers=headers, data=payload)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table in the HTML
    table = soup.find('table', {'class': 'tableFile2'})
    
    if soup.find(class_='companyName') != None:
        
        company_name = str(soup.find(class_='companyName').text).split("CIK#: ")[0].strip()
        company_cik = str(re.findall('\d+', str(soup.find(class_='companyName').text).split("CIK#: ")[1].strip())[0])
        company_state = soup.find(class_='identInfo').text.split("State location: ")[1].split("|")[0].strip()
        df = pd.DataFrame({'CIK': [company_cik], 'Company Name': [company_name], 'State': [company_state]})
        return df
    
    # Extract the table rows
    if isinstance(table, element.Tag):
        rows = table.find_all('tr')

        # Extract the CIK Codes, Company Names and States
        cik_codes = []
        company_names = []
        states = []
        for row in rows[1:]:  # Ignore the header row
            cols = row.find_all('td')
            cik_code = cols[0].text
            company_name = cols[1].text
            state = cols[2].text
            cik_codes.append(cik_code)
            company_names.append(company_name)
            states.append(state)

        # Create a pandas DataFrame
        df = pd.DataFrame({
            'CIK': cik_codes,
            'Company Name': company_names,
            'State': states
        })
        print(f"Start Row: {start_row} - {df.iloc[0]['Company Name']}")
        
        if (comprehensive == True) & (len(df) == 100) & ( last_df.equals(df) == False) & (start_row < max_start_row):
            new_df = edgar_cik(query, comprehensive = comprehensive, start_row = start_row + 100, last_df = df)
                    
            df = pd.concat([df,
                    new_df
                    ]).reset_index(drop=True)

        return df
    
    else:
        print(f"Final Row Reached At {start_row}")
        return pd.DataFrame()


# %%
