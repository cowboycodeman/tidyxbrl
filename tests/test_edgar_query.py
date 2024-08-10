import sys
import os
import pytest
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.tidyxbrl import edgar_cik, edgar_query

@pytest.fixture
def setup_cik():
    return edgar_cik("ZILLOW GROUP, INC.")

def test_edgar_query_submissions():
    ms_sub = edgar_query('0000789019', query_type='submissions')
    assert ms_sub is not None, "Submissions result should not be None"
    assert isinstance(ms_sub,  pd.DataFrame), "Submissions result should be a dataframe"
    assert 'value' in ms_sub, "Submissions result should contain 'value'"

def test_edgar_query_companyconcept():
    ms_concept = edgar_query('0000789019', query_type='companyconcept', queryextension='/us-gaap/AccountsPayableCurrent.json')
    assert ms_concept is not None, "Company concept result should not be None"
    assert isinstance(ms_concept, pd.DataFrame), "Company concept result should be a dataframe"
    assert 'value' in ms_concept, "Company concept should contain 'value'"

def test_edgar_query_companyfacts():
    ms_facts = edgar_query('0000789019', query_type='companyfacts')
    assert ms_facts is not None, "Company facts result should not be None"
    assert isinstance(ms_facts,  pd.DataFrame), "Company facts result should be a dataframe"
    assert 'value' in ms_facts, "Company facts result should contain 'value'"

def test_edgar_query_zillow_submissions(setup_cik):
    desiredcorp = str(setup_cik[setup_cik.company.str.contains("ZILLOW GROUP, INC.")]['cik_str'].unique()[0])
    zillow_sub = edgar_query(desiredcorp, query_type='submissions')
    assert zillow_sub is not None, "Zillow submissions result should not be None"
    assert isinstance(zillow_sub,  pd.DataFrame), "Zillow submissions result should be a dataframe"
    assert 'value' in zillow_sub, "Zillow submissions result should contain 'value'"

def test_edgar_query_zillow_companyconcept(setup_cik):
    desiredcorp = str(setup_cik[setup_cik.company.str.contains("ZILLOW GROUP, INC.")]['cik_str'].unique()[0])
    zillow_concept = edgar_query(desiredcorp, query_type='companyconcept', queryextension='/us-gaap/AccountsPayableCurrent.json')
    assert zillow_concept is not None, "Zillow company concept result should not be None"
    assert isinstance(zillow_concept,  pd.DataFrame), "Zillow company concept result should be a dataframe"
    assert 'value' in zillow_concept, "Zillow company concept result should contain 'value'"

def test_edgar_query_zillow_companyfacts(setup_cik):
    desiredcorp = str(setup_cik[setup_cik.company.str.contains("ZILLOW GROUP, INC.")]['cik_str'].unique()[0])
    zillow_facts = edgar_query(desiredcorp, query_type='companyfacts')
    assert zillow_facts is not None, "Zillow company facts result should not be None"
    assert isinstance(zillow_facts,  pd.DataFrame), "Zillow company facts result should be a dataframe"
    assert 'value' in zillow_facts, "Zillow company facts result should contain 'value'"