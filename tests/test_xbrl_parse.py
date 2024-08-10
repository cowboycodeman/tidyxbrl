# %%
import sys
import os
import pytest
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.tidyxbrl import xbrl_parse

 # %%

def test_xbrl_parse():
    applesecweburl = "https://www.sec.gov/Archives/edgar/data/320193/000032019321000010/aapl-20201226_htm.xml"
    teslasecweburl = "https://www.sec.gov/Archives/edgar/data/1318605/000156459020047486/tsla-10q_20200930_htm.xml"
    ibmsecweburl = "https://www.sec.gov/Archives/edgar/data/51143/000155837020001334/ibm-20191231x10k2af531_htm.xml"

    appledata = xbrl_parse(applesecweburl)
    tesladata = xbrl_parse(teslasecweburl)
    ibmdata = xbrl_parse(ibmsecweburl)

    # Basic assertions to check if data is not None
    assert appledata is not None, "Apple data should not be None"
    assert tesladata is not None, "Tesla data should not be None"
    assert ibmdata is not None, "IBM data should not be None"

    # Check if the data is in the expected format (e.g., dictionary)
    assert isinstance(appledata, pd.DataFrame), "Apple data should be a dataframe"
    assert isinstance(tesladata, pd.DataFrame), "Tesla data should be a dataframe"
    assert isinstance(ibmdata, pd.DataFrame), "IBM data should be a dataframe"

    # Check for specific keys in the parsed data
    for data, company in [(appledata, "Apple"), (tesladata, "Tesla"), (ibmdata, "IBM")]:
        assert 'datacode' in data, f"{company} data should contain 'financials'"
        assert 'datavalue' in data, f"{company} data should contain 'datavalue'"
        assert 'context' in data, f"{company} data should contain 'context'"
        assert 'startDate' in data, f"{company} data should contain 'startDate'"
        assert 'endDate' in data, f"{company} data should contain 'endDate'"
        assert 'segment' in data, f"{company} data should contain 'segment'"
        
# %%
