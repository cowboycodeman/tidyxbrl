import pandas
import requests
from tqdm import tqdm


def edgar_query(companycik, query_type, queryextension=''):
    """
    https://www.sec.gov/edgar/sec-api-documentation
    The edgar_query function is used to query SEC data using the Central Index Key (CIK) determined in the edgar_cik function
    Inputs:
        companycik: Unique company CIK value pulled in edgar_cik. Note that the CIK is converted to 10 digits with leading 0s
        query_type: The type of API query:
            - submissions: Each entity’s current filing history
            - companyconcept: The company-concept API returns all the XBRL disclosures from a single company (CIK) and concept (a taxonomy and tag) into a single JSON file, with a separate array of facts for each units on measure that the company has chosen to disclose
            - companyfacts: This API returns all the company concepts data for a company into a single API call
        queryextension: Extension required for the "companyconcept" query_type to specify the report type

    Outputs:
        longdata: Tidy dataframe housing the report data

    Examples:
        - edgar_query('0000789019', query_type = 'submissions')
        - edgar_query('0000789019', query_type = 'companyconcept', queryextension = '/us-gaap/AccountsPayableCurrent.json')
        - edgar_query('0000789019', query_type = 'companyfacts')
    """

    # Pull one of the urls associated with the query types
    querydict = {'submissions': 'https://data.sec.gov/submissions/CIK',
                 'companyconcept': 'https://data.sec.gov/api/xbrl/companyconcept/CIK',
                 'companyfacts': 'https://data.sec.gov/api/xbrl/companyfacts/CIK'}
    # Raise error if the data does not exist
    if query_type not in querydict.keys():
        raise ValueError("parse_type must be in: " + str(querydict.keys()))
    # Specify the query url and parameters
    urlquery = querydict[query_type]
    dataquery = urlquery + str(companycik) + \
        str(queryextension).replace(".json", "") + ".json"
    soupheaders = {'User-Agent': 'Mozilla'}
    # Pull the data, check the response, and convert to a long format
    dataresponse = requests.get(url=dataquery, headers=soupheaders)
    if dataresponse.status_code == 200:
        try:
            result = pandas.DataFrame(pandas.json_normalize(dataresponse.json()))
            longdata = pandas.melt(result, id_vars=['cik'])
        except Exception:
            raise ValueError(str(dataresponse.json()))
    else:
        xbrl_queryoutput = dataresponse.status_code
        print(dataresponse.text)
        raise ValueError(str(xbrl_queryoutput) + ": Error in Response")
    
    # If the data is in a list form, then convert into a nested dataframe
    for valueholder in tqdm(range(1, longdata.value.__len__())):
        loadvalue = longdata.iloc[valueholder].value
        if(str(type(loadvalue)) == "<class 'list'>" and loadvalue.__len__() > 1):
            try:
                longdata.at[valueholder, 'value'] = (
                    pandas.json_normalize(loadvalue))
            except:
                pass

    return longdata
