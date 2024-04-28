import pandas
import requests
from tqdm import tqdm


def edgar_frames(urldescriptor=""):
    """
    The edgar_frames function aggregates one fact for each reporting entity that is last filed that most closely fits the calendrical period requested. This API supports for annual, quarterly and instantaneous data

    Inputs:
        urldescriptor: URL description of the frame query (everything after https://data.sec.gov/api/xbrl/frames/). The data is structured as "finstandard/reporttype/denomination/dateholder"
            - finstandard: The financial reporting standard
                * us-gaap
                * ifrs-full
                * dei
                * srt
            - reporttype: The type of report to query. See the 'datacode' column returned in the xbrl_parse function (i.e. NonoperatingIncomeExpense)
            - denomination: Report currency (i.e. USD)
            - dateholder: Date of evaluation (i.e. CY2019Q1I)

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
    soupheaders = {"User-Agent": "Mozilla"}
    # Pull the data, check the response, and convert to a long format
    dataresponse = requests.get(url=dataquery, headers=soupheaders)
    if dataresponse.status_code == 200:
        try:
            result = pandas.DataFrame(pandas.json_normalize(dataresponse.json()))
            longdata = pandas.melt(result, id_vars=["taxonomy"])
        except Exception:
            raise ValueError(str(dataresponse.json()))
    else:
        xbrl_queryoutput = dataresponse.status_code
        print(dataresponse.text)
        raise ValueError(str(xbrl_queryoutput) + ": Error in Response")

    # If the data is in a list form, then convert into a nested dataframe
    for valueholder in tqdm(range(1, longdata.value.__len__())):
        loadvalue = longdata.iloc[valueholder].value
        if str(type(loadvalue)) == "<class 'list'>" and loadvalue.__len__() > 1:
            try:
                longdata.at[valueholder, "value"] = pandas.json_normalize(loadvalue)
            except:
                pass

    return longdata
