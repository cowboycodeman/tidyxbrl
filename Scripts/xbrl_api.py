# xbrl get key
# xbrl get sec-url
# xbrl get sec url
# get xbrl key

import requests

username = 'mcdonald.ryan@hotmail.com'
password = 'Mcawesome1*'
client_id = '078175dd-64d2-4bd1-9dbe-6251a4f56eb5'
client_secret = '22980c97-8fea-46dd-a374-3d2954413b90'

def xbrl_apikey(username, password, client_id,client_secret,platform = 'pc', grant_type = 'password'):

    platform = 'pc'
    grant_type = 'password'

    response = requests.post(url='https://api.xbrl.us/oauth2/token', data={'grant_type': grant_type,
                                                                'client_id': client_id,
                                                                'client_secret': client_secret,
                                                                'username': username,
                                                                'password': password,
                                                                'platform': platform
                                                                } )

    result = pandas.DataFrame(pandas.json_normalize(response.json()))

    try:
        global bearertolken
        global refreshtolken
        bearertolken = result.access_token.values[0]
        refreshtolken = result.refresh_token.values[0]
    except:
        pass

    return result








class filterparams:

    def __init__(self,period_start):
        self.period_start = period_start

    



class queryparams
    def __init__(self, realpart, imagpart):



def xbrl_query(bearertolken, filterparams, queryparams):





    return

