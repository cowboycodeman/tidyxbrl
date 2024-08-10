"""
https://xbrl.us/home/use/xbrl-api/access-token/

API key generation to pull data from the XBRL US API.

"""

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
    timeout_sec = 15
):
    """
    The xbrl_apikey function generates or refreshes a temporary token for the xbrl_apiquery
    function.

    Args:
        username (str): Email address corresponding to the xbrl.us api website.
        password (str): Password corresponding to the xbrl.us api website.
        client_id (str): Active public Client ID.
        client_secret (str): Secret ID corresponding to the client_id.
        platform (str): Keyword to distinguish if the user is authenticating from different
        applications.
        grant_type (str): Either 'password' to generate a new key, or 'refresh_token' to
        refresh an existing key.
        refresh_token (str, optional): Optional refresh token provided in a previous
        xbrl_apikey request.
        timeout_sec: The time in seconds to wait for the server to respond
        con_headers (dict): The headers to be sent with the initial request.

    Returns:
        pandas.DataFrame: DataFrame output of the XBRL api key.
            - platform: Keyword to distinguish if the user is authenticating from different
            applications.
            - access_token: Access token to be passed to the xbrl_apiquery function.
            - refresh_token: Refresh token to refresh the 'access_token'.
            - expires_in: Seconds until expiry.
            - refresh_token_expires_in token_type: Seconds until refresh token expiry.
            - token_type: type of token. Always "bearer".

    Examples:
        xbrl_apikeyoutput = xbrl_apikey(username='username', password='password',
        client_id='client_id', client_secret='client_secret', platform='pc',
        grant_type='password', refresh_token='optional_refresh_token')
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
            timeout=timeout_sec
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
            timeout=timeout_sec
        )
    else:
        raise ValueError("grant_type must be either 'password' or 'refresh_token'")
    # Check the Response Code. 200 is a success
    if xbrl_apikeyoutput.status_code == 200:
        try:
            result = pandas.DataFrame(pandas.json_normalize(xbrl_apikeyoutput.json()))
        except Exception as exc:
            raise ValueError(str(xbrl_apikeyoutput.json())) from exc
    else:
        result = xbrl_apikeyoutput.status_code
        print(xbrl_apikeyoutput.text)
        raise ValueError(str(result) + ": Error in Response")
    return result
