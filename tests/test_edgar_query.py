import sys
import os
import pytest
from tidyxbrl import edgar_cik, edgar_query

def test_edgar_query():
    ms_sub = edgar_query('0000789019', query_type='submissions')
    ms_concept = edgar_query('0000789019', query_type='companyconcept', queryextension='/us-gaap/AccountsPayableCurrent.json')
    ms_facts = edgar_query('0000789019', query_type='companyfacts')

    companycik = edgar_cik("ZILLOW GROUP, INC.")
    desiredcorp = str(companycik[companycik.company.str.contains("ZILLOW GROUP, INC.")]['cik_str'].unique()[0])
    zillow_sub = edgar_query(desiredcorp, query_type='submissions')
    zillow_concept = edgar_query(desiredcorp, query_type='companyconcept', queryextension='/us-gaap/AccountsPayableCurrent.json')
    zillow_facts = edgar_query(desiredcorp, query_type='companyfacts')

# %%
