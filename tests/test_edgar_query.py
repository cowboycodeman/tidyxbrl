import tidyxbrl

companycik = tidyxbrl.edgar_cik()

tidyxbrl.edgar_query('0000789019', query_type = 'submissions')
tidyxbrl.edgar_query('0000789019', query_type = 'companyconcept', queryextension = '/us-gaap/AccountsPayableCurrent.json')
tidyxbrl.edgar_query('0000789019', query_type = 'companyfacts')

desiredcorp = str(companycik[companycik.title.str.contains("ZILLOW GROUP, INC.")]['cik_str'].unique()[0])

tidyxbrl.edgar_query(desiredcorp, query_type = 'submissions')
tidyxbrl.edgar_query(desiredcorp, query_type = 'companyconcept', queryextension = '/us-gaap/AccountsPayableCurrent.json')
tidyxbrl.edgar_query(desiredcorp, query_type = 'companyfacts')