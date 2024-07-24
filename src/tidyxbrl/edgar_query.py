"""
https://www.sec.gov/edgar/sec-api-documentation

data.sec.gov/submissions/
Each entity’s current filing history is available at the following URL:
https://data.sec.gov/submissions/CIK##########.json
Where the ########## is the entity’s 10-digit Central Index Key (CIK), including leading
zeros.

This JSON data structure contains metadata such as current name, former name, and stock
exchanges and ticker symbols of publicly-traded companies. The object’s property path
contains at least one year’s of filing or to 1,000 (whichever is more) of the most recent
filings in a compact columnar data array. If the entity has additional filings, files will
contain an array of additional JSON files and the date range for the filings each one
contains.

------

data.sec.gov/api/xbrl/companyconcept/
The company-concept API returns all the XBRL disclosures from a single company (CIK) and
concept (a taxonomy and tag) into a single JSON file, with a separate array of facts for
each units on measure that the company has chosen to disclose (e.g. net profits reported
in U.S. dollars and in Canadian dollars).

https://data.sec.gov/api/xbrl/companyconcept/CIK##########/us-gaap/AccountsPayableCurrent.json

-----

data.sec.gov/api/xbrl/companyfacts/
This API returns all the company concepts data for a company into a single API call:

https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json
"""

import pandas
import requests
from tqdm import tqdm
import numpy


def edgar_query(companycik, query_type, queryextension="", parse_pandas = True, timeout_sec = 15):
    """
    Query SEC data using the Central Index Key (CIK).

    The edgar_query function is used to query SEC data using the Central Index Key (CIK)
    determined in the edgar_cik function.

    Args:
        companycik (str): Unique company CIK value pulled in edgar_cik. Note that the CIK is
        converted to 10 digits with leading 0s.
        query_type (str): The type of API query. Can be 'submissions', 'companyconcept', or
        'companyfacts'.
        queryextension (str, optional): Extension required for the "companyconcept"
        query_type to specify the report type. Defaults to "".
        parse_pandas (bool, optional): If True, the data is converted to a pandas DataFrame.
        timeout_sec: The time in seconds to wait for the server to respond

    Returns:
        pandas.DataFrame: Tidy dataframe housing the report data.

    Raises:
        ValueError: If query_type is not one of 'submissions', 'companyconcept', or
        'companyfacts'.

    Examples:
        edgar_query('0000789019', query_type = 'submissions')
        edgar_query('0000789019', query_type = 'companyconcept',
        queryextension = '/us-gaap/AccountsPayableCurrent.json')
        edgar_query('0000789019', query_type = 'companyfacts')
    """

    # Pull one of the urls associated with the query types
    querydict = {
        "submissions": "https://data.sec.gov/submissions/CIK",
        "companyconcept": "https://data.sec.gov/api/xbrl/companyconcept/CIK",
        "companyfacts": "https://data.sec.gov/api/xbrl/companyfacts/CIK",
    }
    # Raise error if the data does not exist
    if query_type not in querydict:
        raise ValueError("parse_type must be in: " + str(querydict))
    # Specify the query url and parameters
    urlquery = querydict[query_type]
    dataquery = (
        urlquery + str(companycik) + str(queryextension).replace(".json", "") + ".json"
    )
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "DNT": "1",  # Do Not Track Request Header
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    # Pull the data, check the response, and convert to a long format
    dataresponse = requests.get(url=dataquery, headers=headers, timeout=timeout_sec)
    if dataresponse.status_code == 200:
        try:
            result = pandas.DataFrame(pandas.json_normalize(dataresponse.json()))
            longdata = pandas.melt(result, id_vars=["cik"])
        except Exception as exc:
            raise ValueError(str(dataresponse.json())) from exc
    else:
        xbrl_queryoutput = dataresponse.status_code
        # print(dataresponse.text)
        raise ValueError(str(xbrl_queryoutput) + ": " + str(dataresponse.content))

    # If the data is in a list form, then convert it into a nested dataframe
    if parse_pandas:
        for valueholder in tqdm(range(1, len(longdata.value))):
            loadvalue = longdata.iloc[valueholder].value
            if isinstance(loadvalue, list):
                try:
                    loadvalue_df = pandas.DataFrame(loadvalue)
                    if len(loadvalue_df) > 1:
                        loadvalue_df = loadvalue_df.transpose().explode("value")
                    longdata.at[valueholder, "value"] = loadvalue_df
                except Exception:
                    longdata.at[valueholder, "value"] = pandas.DataFrame(loadvalue)
    longdata = longdata.assign(cik = lambda x: pandas.to_numeric(x.cik, errors='coerce'))
    return longdata
