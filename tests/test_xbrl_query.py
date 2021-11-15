import yaml
import tidyxbrl 

credentials = yaml.safe_load(open("tests\test_credentials.yml", "r"))
username = credentials['credentials']['username'][0]
password = credentials['credentials']['password'][0]
client_id = credentials['credentials']['client_id'][0]
client_secret = credentials['credentials']['client_secret'][0]

response = tidyxbrl.xbrl_apikey(username=username, password=password, client_id=client_id, client_secret=client_secret, platform='pc', grant_type='password', refresh_token='')

dataresponse = tidyxbrl.xbrl_query(access_token=response.access_token.values[0], 
               baseapiurl='https://api.xbrl.us/api/v1/report/search?',
               queryparameters = {'report.entity-name': "APPLE INC.",
                                  'fields': "report.id,report.entity-name,report.filing-date,report.base-taxonomy,report.document-type,report.accession,entity.ticker,report.sic-code,entity.cik,report.entry-type,report.period-end,report.sec-url,report.checks-run,report.accepted-timestamp.sort(DESC),report.limit(20),report.offset(0),dts.id,report.entry-url",
                                  'report.document-type': "10-K"
                        })

dataresponse2 = tidyxbrl.xbrl_query(access_token=response.access_token.values[0], 
               baseapiurl='https://api.xbrl.us/api/v1/fact/search?',
               queryparameters = {'report.id': "315201",
                                  'fields': "report.id,report.entity-name,report.filing-date,report.base-taxonomy,report.document-type,report.accession,entity.ticker,report.sic-code,entity.cik,report.entry-type,report.period-end,report.sec-url,report.checks-run,report.accepted-timestamp.sort(DESC),report.limit(20),report.offset(0),dts.id,report.entry-url",
                                  'concept.local-name': "AccumulatedOtherComprehensiveIncomeLossNetOfTax"
                        })


dataresponse3 = tidyxbrl.xbrl_query(access_token=response.access_token.values[0], 
               baseapiurl='https://api.xbrl.us/api/v1/fact/141024005?',
               queryparameters = {'fields': "fact.value,concept.local-name"
                        })
