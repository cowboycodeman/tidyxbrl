<div align="center">
  <img src="https://www.xbrl.org/wp-content/themes/xbrl/images/logoHeader.png"><br>
</div>

-----------------

# tidyxbrl: The tidy XBRL Interface

## What is it?

**tidyxbrl** is a Python package that parses XBRL data files and returns dynamic structures that succinctly store the underlying data. This package additionally can interface with the XBRL API and SEC EDGAR interfaces, with further expansion to other XBRL data providers planned for the near future. This package aims to the be the simplest and most effective method to parse XBRL data in Python.

## The XBRL Standard
eXtensible Business Reporting Language (XBRL) is a standardized financial reporting framework to structure financial reporting in a way that enables automation and machine processing. This package aims to enable its users to realize the full capabilities of the XBRL standard through parsing files and interfacing with the applicable APIs.

Applicable documentation can be found below:
### XBRL
  - [**XBRL API Overview**][xbrl-api-url]
  - [**XBRL API Documentation**][xbrl-documentation-url]
  - [**XBRL API Examples**][xbrl-example-url]

### EDGAR
  - [**SEC Edgar Information**][sec-edgar-data-url]
  - [**SEC API Documentation**][sec-api-documentation-url]
  - [**SEC Flat Files**][sec-flatfiles-url]
  
  [xbrl-api-url]: https://xbrl.us/home/use/xbrl-api/
  [xbrl-documentation-url]: http://files.xbrl.us/documents/XBRL-API-V1.4.pdf
  [xbrl-example-url]: https://xbrlus.github.io/xbrl-api/#/document/getDocumentInfo
  [sec-edgar-data-url]: https://www.sec.gov/os/accessing-edgar-data
  [sec-api-documentation-url]: https://www.sec.gov/edgar/sec-api-documentation
  [sec-flatfiles-url]: https://www.sec.gov/Archives/edgar/full-index/

## Where to get it
The source code is currently hosted on GitHub at:
https://github.com/cowboycodeman/tidyxbrl/

The tidyxbrl package is publically available for download at:
https://pypi.org/project/tidyxbrl/

```sh
# PyPI
pip install tidyxbrl
```
## Examples
**xbrl_parse** - Parse xbrl files or website urls
```
tidyxbrl.xbrl_parse("https://www.sec.gov/Archives/edgar/data/320193/000032019321000010/aapl-20201226_htm.xml")
```

**xbrl_query** - Query the XBRL API
```
response = tidyxbrl.xbrl_apikey(username=username, password=password, client_id=client_id, client_secret=client_secret, platform='pc', grant_type='password', refresh_token='')
dataresponse = tidyxbrl.xbrl_query(access_token=response.access_token.values[0], 
               baseapiurl='https://api.xbrl.us/api/v1/report/search?',
               queryparameters = {'report.entity-name': "APPLE INC.",
                                  'fields': "report.id,report.entity-name,report.filing-date,report.base-taxonomy,report.document-type,report.accession,entity.ticker,report.sic-code,entity.cik,report.entry-type,report.period-end,report.sec-url,report.checks-run,report.accepted-timestamp.sort(DESC),report.limit(20),report.offset(0),dts.id,report.entry-url",
                                  'report.document-type': "10-K"
                        })
```

**edgar_query** - Query SEC data using the Central Index Key (CIK)
```
companycik = tidyxbrl.edgar_cik()
desiredcorp = str(companycik[companycik.title.str.contains("ZILLOW GROUP, INC.")]['cik_str'].unique()[0])
tidyxbrl.edgar_query(desiredcorp, query_type = 'submissions')
tidyxbrl.edgar_query(desiredcorp, query_type = 'companyconcept', queryextension = '/us-gaap/AccountsPayableCurrent')
tidyxbrl.edgar_query(desiredcorp, query_type = 'companyfacts')
```

**edgar_frames** - Aggregates one fact for each reporting entity
```
tidyxbrl.edgar_frames(urldescriptor = 'us-gaap/NonoperatingIncomeExpense/USD/CY2019Q1I')
```

## Dependencies
- [pandas - A fast, powerful, flexible and easy to use open source data analysis and manipulation tool, built on top of the Python programming language.](https://pandas.pydata.org/)
- [NumPy - The fundamental package for scientific computing with Python](https://www.numpy.org)
- [requests - An elegant and simple HTTP library for Python, built for human beings.](https://docs.python-requests.org/en/master/)
- [bs4 - For pulling data out of HTML and XML files](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
