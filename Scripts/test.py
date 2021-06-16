exec(open("Scripts/read_xbrl.py").read())
exec(open("Scripts/read_xbrlxml.py").read())
pandas.set_option('display.max_columns', None)
pandas.set_option('display.max_colwidth', None)
# pandas.set_option('display.max_rows', 500)
# pandas.set_option('display.min_rows', 200)
#
# import read_xbrl


apikey = "53c0453a-46f2-4526-96e1-67f3057190bf"


applesecweburl = "https://www.sec.gov/Archives/edgar/data/320193/000032019321000010/aapl-20201226_htm.xml"
teslasecweburl = "https://www.sec.gov/Archives/edgar/data/1318605/000156459020047486/tsla-10q_20200930_htm.xml"

appledata = read_xbrlxml(applesecweburl)
tesladata = read_xbrl(teslasecweburl)

ibmdata = read_xbrl("https://www.sec.gov/Archives/edgar/data/51143/000155837020001334/ibm-20191231x10k2af531_htm.xml")

ibmdata[ibmdata.context == "As_Of_12_31_2017_f3wZQVMq4UyGjD75opLv4A"]

holder = read_xbrl(applesecweburl)

yoloout = data_assign(holder)


if __name__ == '__main__':
    #partial_data_assign = partial(data_assign, outputframe)
    pool = Pool()
    dataout = pool.map(partial_data_assign,  outputframe)
    pool.close()
    pool.join()
