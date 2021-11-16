import pandas
import requests

# Function to query the XBRL API


def xbrl_query(access_token,
               queryparameters,
               baseapiurl='https://api.xbrl.us/api/v1/report/search?'):
    """
    https://xbrl.us/home/use/xbrl-api/
    http://files.xbrl.us/documents/XBRL-API-V1.4.pdf

    The xbrl_query function is used to query the xbrl api usingthe token generated in the xbrl_apikey function. 
    Inputs:
        access_token: Access token string generated in the xbrl_apikey function. Found in the access_token column of the response dataframe.
        baseapiurl: API request URL corresponding to the type of request prior to passing any parameters. This is everything up-to and including the "?" in the API request
            - 'https://api.xbrl.us/api/v1/report/search?'
            - 'https://api.xbrl.us/api/v1/fact/search?'
        queryparameters: Dictionary structure to specify each aspect of the api request (See the Examples section below)

    Outputs:
        xbrl_queryoutput: Pandas Dataframe object corresponding to the fields specified in the request

    Examples:
        - xbrl_query(access_token=xbrl_apikeyoutput.access_token.values[0], 
                        baseapiurl='https://api.xbrl.us/api/v1/report/search?',
                        queryparameters = {'report.entity-name': "APPLE INC.",
                                        'fields': "report.id,report.entity-name,report.filing-date,report.base-taxonomy,report.document-type,report.accession,entity.ticker,report.sic-code,entity.cik,report.entry-type,report.period-end,report.sec-url,report.checks-run,report.accepted-timestamp.sort(DESC),report.limit(20),report.offset(0),dts.id,report.entry-url",
                                        'report.document-type': "10-K"
                            })
        - xbrl_query(access_token=xbrl_apikeyoutput.access_token.values[0], 
                        baseapiurl='https://api.xbrl.us/api/v1/fact/search?',
                        queryparameters = {'report.id': "315201",
                                        'fields': "report.id,report.entity-name,report.filing-date,report.base-taxonomy,report.document-type,report.accession,entity.ticker,report.sic-code,entity.cik,report.entry-type,report.period-end,report.sec-url,report.checks-run,report.accepted-timestamp.sort(DESC),report.limit(20),report.offset(0),dts.id,report.entry-url",
                                        'concept.local-name': "AccumulatedOtherComprehensiveIncomeLossNetOfTax"
                                })

    """

    # Modify the queryparameter keys to create a web request string in dataquery
    # Add the "=" sign between keys and values
    for keyholder in list(queryparameters.keys()):
        queryparameters[keyholder + "="] = queryparameters[keyholder]
        del queryparameters[keyholder]
    # Add the "&" sign between keys
    queryurl = ''.join(list(map(str.__add__, list(queryparameters.keys()), [
                       "{}{}".format(i, '&') for i in list(queryparameters.values())])))[:-1]
    # Add the baseurl and modified request values
    dataquery = str(baseapiurl + queryurl)
    # Generate the authentication bearer tolken
    headers = {"Authorization": "Bearer " + access_token}
    # Generate the response
    dataresponse = requests.get(url=dataquery, headers=headers)
    # Check the Response Code
    if dataresponse.status_code == 200:
        try:
            xbrl_queryoutput = pandas.DataFrame.from_dict(
                dataresponse.json()['data'])
        except Exception:
            raise ValueError(dataresponse.json())
    else:
        xbrl_queryoutput = dataresponse.status_code
        print(dataresponse.text)
        raise ValueError(xbrl_queryoutput + ": Error in Response")
    return(xbrl_queryoutput)
