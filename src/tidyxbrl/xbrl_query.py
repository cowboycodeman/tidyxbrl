"""

https://xbrlus.github.io/xbrl-api/

Query functions for the XBRL API
"""

import pandas
import requests
from src.config.default_headers import con_headers_default


def xbrl_query(
    access_token,
    queryparameters,
    baseapiurl="https://api.xbrl.us/api/v1/report/search?",
    timeout_sec = 15,
    con_headers = con_headers_default
):
    """
    https://xbrl.us/home/use/xbrl-api/
    http://files.xbrl.us/documents/XBRL-API-V1.4.pdf

    The xbrl_query function is used to query the xbrl api using the token generated in the
    xbrl_apikey function.

    Args:
        access_token: Access token string generated in the xbrl_apikey function. Found in the
        access_token column of the response dataframe.
        baseapiurl: API request URL corresponding to the type of request prior to passing any
        parameters. This is everything up-to and including the "?" in the API request
            - 'https://api.xbrl.us/api/v1/report/search?'
            - 'https://api.xbrl.us/api/v1/fact/search?'
        queryparameters: Dictionary structure to specify each aspect of the api request (See the
        Examples section below)
        con_headers (dict): The headers to be sent with the initial request.

    Outputs:
        xbrl_queryoutput: Pandas Dataframe object corresponding to the fields specified in the
        request

    Examples:
        - xbrl_query(access_token=xbrl_apikeyoutput.access_token.values[0],
                    baseapiurl='https://api.xbrl.us/api/v1/report/search?',
                    queryparameters = {'report.entity-name': "APPLE INC.",
                                        'fields': "report.id,report.entity-name,report.filing-date,
                                        report.base-taxonomy,report.document-type,report.accession,
                                        entity.ticker,report.sic-code,entity.cik,report.entry-type,
                                        report.period-end,report.sec-url,report.checks-run,
    """

    # Modify the queryparameter keys to create a web request string in dataquery
    # Add the "=" sign between keys and values
    for keyholder in list(queryparameters.keys()):
        queryparameters[keyholder + "="] = queryparameters[keyholder]
        del queryparameters[keyholder]
    # Add the "&" sign between keys
    queryurl = "".join(
        [f"{key}{value}&" for key, value in queryparameters.items()]
    )[:-1]
    # Add the baseurl and modified request values
    dataquery = str(baseapiurl + queryurl)
    # Generate the authentication bearer tolken
    headers =  {**con_headers, **{"Authorization": "Bearer " + access_token}}
    # Generate the response
    dataresponse = requests.get(url=dataquery, headers=headers, timeout=timeout_sec)
    # Check the Response Code
    if dataresponse.status_code == 200:
        try:
            xbrl_queryoutput = pandas.DataFrame.from_dict(dataresponse.json()["data"])
        except Exception as exc:
            raise ValueError(str(dataresponse.json())) from exc
    else:
        xbrl_queryoutput = dataresponse.status_code
        print(dataresponse.text)
        raise ValueError(str(xbrl_queryoutput) + ": Error in Response")
    return xbrl_queryoutput
