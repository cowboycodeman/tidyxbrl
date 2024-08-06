"""
https://www.sec.gov/edgar/sec-api-documentation

data.sec.gov/api/xbrl/frames/
The xbrl/frames API aggregates one fact for each reporting entity that is last filed
that most closely fits the calendrical period requested. This API supports for annual,
quarterly and instantaneous data:

https://data.sec.gov/api/xbrl/frames/us-gaap/AccountsPayableCurrent/USD/CY2019Q1I.json
Where the units of measure specified in the XBRL contains a numerator and a denominator,
these are separated by “-per-” such as “USD-per-shares”. Note that the default unit in
XBRL is “pure”.

The period format is CY#### for annual data (duration 365 days +/- 30 days), CY####Q# for
quarterly data (duration 91 days +/- 30 days), and CY####Q#I for instantaneous data.
Because company financial calendars can start and end on any month or day and even change
in length from quarter to quarter to according to the day of the week, the frame data is
assembled by the dates that best align with a calendar quarter or year. Data users should
be mindful different reporting start and end dates for facts contained in a frame.
"""

import pandas
import requests
from tqdm import tqdm
from src.config.default_headers import con_headers_default


def edgar_frames(urldescriptor="", timeout_sec = 15, con_headers = con_headers_default):
    """
    The edgar_frames function aggregates one fact for each reporting entity
    that is last filed that most closely fits the calendrical period requested.
    This API supports for annual, quarterly and instantaneous data

    Args:
        urldescriptor: URL description of the frame query
        (everything after https://data.sec.gov/api/xbrl/frames/***)
        The data is structured as "finstandard/reporttype/denomination/dateholder"
        
            - finstandard: The financial reporting standard
                * us-gaap
                * ifrs-full
                * dei
                * srt
            - reporttype: Type of report. See datacode in xbrl_parse (i.e. NonoperatingIncomeExpense)
            - denomination: Report currency (i.e. USD)
            - dateholder: Date of evaluation (i.e. CY2019Q1I)
        timeout_sec: The time in seconds to wait for the server to respond

    Outputs:
        return companies: Return a pandas DataFrame of reporting companies and their associated CIK

    Examples:
        - edgar_frames(urldescriptor = 'us-gaap/NonoperatingIncomeExpense/USD/CY2019Q1I.json')
    """

    # Specify the query url and parameters
    dataquery = (
        "https://data.sec.gov/api/xbrl/frames/"
        + str(urldescriptor).replace(".json", "")
        + ".json"
    )
    # Pull the data, check the response, and convert to a long format
    dataresponse = requests.get(url=dataquery, headers=con_headers, timeout=timeout_sec)
    if dataresponse.status_code == 200:
        try:
            result = pandas.DataFrame(pandas.json_normalize(dataresponse.json()))
            longdata = pandas.melt(result, id_vars=["taxonomy"])
        except Exception as exc:
            raise ValueError(f"Error in parsing JSON response: {str(dataresponse.json())}") from exc
    else:
        xbrl_queryoutput = dataresponse.status_code
        print(dataresponse.text)
        raise ValueError(str(xbrl_queryoutput) + ": Error in Response")

    # If the data is in a list form, then convert into a nested dataframe
    for valueholder in tqdm(range(1, len(longdata))):
        loadvalue = longdata.iloc[valueholder].value
        if str(type(loadvalue)) == "<class 'list'>" and len(loadvalue) > 1:
            try:
                longdata.at[valueholder, "value"] = pandas.json_normalize(loadvalue)
            except ValueError:
                pass

    return longdata
