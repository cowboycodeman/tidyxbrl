import pytest
import tidyxbrl 

def test_xbrl_parse():
    applesecweburl = "https://www.sec.gov/Archives/edgar/data/320193/000032019321000010/aapl-20201226_htm.xml"
    teslasecweburl = "https://www.sec.gov/Archives/edgar/data/1318605/000156459020047486/tsla-10q_20200930_htm.xml"
    ibmsecweburl = "https://www.sec.gov/Archives/edgar/data/51143/000155837020001334/ibm-20191231x10k2af531_htm.xml"

    appledata = tidyxbrl.xbrl_parse(applesecweburl)
    tesladata = tidyxbrl.xbrl_parse(teslasecweburl)
    ibmdata = tidyxbrl.xbrl_parse(ibmsecweburl)

    # Add your assertions here
    assert appledata is not None
    assert tesladata is not None
    assert ibmdata is not None

# %%
