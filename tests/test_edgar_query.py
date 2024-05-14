import tidyxbrl

def test_edgar_query():
    ms_sub = tidyxbrl.edgar_query('0000789019', query_type='submissions')
    ms_concept = tidyxbrl.edgar_query('0000789019', query_type='companyconcept', queryextension='/us-gaap/AccountsPayableCurrent.json')
    ms_facts = tidyxbrl.edgar_query('0000789019', query_type='companyfacts')

    companycik = tidyxbrl.edgar_cik("ZILLOW GROUP, INC.")
    desiredcorp = str(companycik[companycik.company.str.contains("ZILLOW GROUP, INC.")]['cik_str'].unique()[0])
    zillow_sub = tidyxbrl.edgar_query(desiredcorp, query_type='submissions')
    zillow_concept = tidyxbrl.edgar_query(desiredcorp, query_type='companyconcept', queryextension='/us-gaap/AccountsPayableCurrent.json')
    zillow_facts = tidyxbrl.edgar_query(desiredcorp, query_type='companyfacts')
