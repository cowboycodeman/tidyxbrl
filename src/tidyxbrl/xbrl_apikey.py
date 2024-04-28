import pandas
import requests


def xbrl_apikey(
    username,
    password,
    client_id,
    client_secret,
    platform="pc",
    grant_type="password",
    refresh_token="",
):
    """
    The xbrl_apikey function is used to generate or refresh a temporary tolken to be used with the xbrl_apiquery function
    Inputs:
        username: Email address corresponding to the xbrl.us api website
        password: Password corresponding to the xbrl.us api website
        client_id: Active public Client ID
        client_secret: Secret ID corresponding to the client_id above
        platform: Keyword to distinguish if the user is authenticating from different applications
        grant_type: Either 'password' to generate a new key, or 'refresh_token' to refresh an existing key (see refresh_token)
        refresh_token: Optional refresh token provided in a previous xbrl_apikey request

    Outputs:
        xbrl_apikeyoutput: Pandas DataFrame output of the XBRL api key
            - platform: Keyword to distinguish if the user is authenticating from different applications (specified in the request)
            - access_token: Access token to be passed to the xbrl_apiquery function
            - refresh_token: Refresh token to refresh the 'access_token'. Can be passed back to the function with a 'refresh_token' grant_type
            - expires_in: Seconds until expiry
            - refresh_token_expires_in token_type: Seconds until refresh token expiry
            - token_type: type of token. Always "bearer"

    The apikey can be accessed in the abrl_apiquery function using: access_token=xbrl_apikeyoutput.access_token.values[0]

    Examples:
        xbrl_apikeyoutput = xbrl_apikey(username='username', password='password', client_id='client_id', client_secret='client_secret', platform='pc', grant_type='password', refresh_token='optional_refresh_token')
    """

    # Submit the request based on the grant_type
    # If password, generate a new tolken
    if grant_type == "password":
        xbrl_apikeyoutput = requests.post(
            url="https://api.xbrl.us/oauth2/token",
            data={
                "grant_type": grant_type,
                "client_id": client_id,
                "client_secret": client_secret,
                "username": username,
                "password": password,
                "platform": platform,
            },
        )
    # If refresh_token, refresh an existing token
    elif grant_type == "refresh_token":
        xbrl_apikeyoutput = requests.post(
            url="https://api.xbrl.us/oauth2/token",
            data={
                "grant_type": grant_type,
                "client_id": client_id,
                "client_secret": client_secret,
                "refresh_token": refresh_token,
                "platform": platform,
            },
        )
    else:
        raise ValueError("grant_type must be either 'password' or 'refresh_token'")
    # Check the Response Code. 200 is a success
    if xbrl_apikeyoutput.status_code == 200:
        try:
            result = pandas.DataFrame(pandas.json_normalize(xbrl_apikeyoutput.json()))
        except Exception:
            raise ValueError(str(dataresponse.json()))
    else:
        result = xbrl_apikeyoutput.status_code
        print(xbrl_apikeyoutput.text)
        raise ValueError(str(result) + ": Error in Response")
    return result
