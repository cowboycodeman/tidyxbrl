# %%
import tidyxbrl

tidyxbrl.edgar_query('0000789019', query_type = 'submissions')
tidyxbrl.edgar_query('0000789019', query_type = 'companyconcept', queryextension = '/us-gaap/AccountsPayableCurrent.json')
tidyxbrl.edgar_query('0000789019', query_type = 'companyfacts')

companycik = tidyxbrl.edgar_cik("ZILLOW GROUP, INC.")
desiredcorp = str(companycik[companycik.company.str.contains("ZILLOW GROUP, INC.")]['cik_str'].unique()[0])
tidyxbrl.edgar_query(desiredcorp, query_type = 'submissions')
tidyxbrl.edgar_query(desiredcorp, query_type = 'companyconcept', queryextension = '/us-gaap/AccountsPayableCurrent.json')
tidyxbrl.edgar_query(desiredcorp, query_type = 'companyfacts')