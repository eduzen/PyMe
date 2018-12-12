import os
import requests
import ssl
from requests_toolbelt import SSLAdapter
from configparser import SafeConfigParser


class PyMe(object):
    def __init__(self, client_id, client_secret, access_token=None, refresh_token=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_in = None
        self._requests = requests.Session()
        # Try to force requests to use the TLSv1 
        try:
            self._requests.mount('https://', SSLAdapter(ssl.PROTOCOL_TLSv1))
        except:
            self._requests = requests
            
        parser = SafeConfigParser()
        parser.read(os.path.dirname(os.path.abspath(__file__))+'/config.ini')

        self.API_ROOT_URL = parser.get('config', 'api_root_url')
        self.SDK_VERSION = parser.get('config', 'sdk_version')
        self.AUTH_URL = parser.get('config', 'auth_url')
        self.OAUTH_URL = parser.get('config', 'oauth_url')
    
    def auth_url(self,redirect_URI):
        params = {
            'client_id':self.client_id,
            'response_type':'code',
            'redirect_uri':redirect_URI}
        url = self.AUTH_URL  + '/authorization' + '?' + urlencode(params)
        return url

    def authorize(self, code, redirect_URI):
        params = { 'grant_type' : 'authorization_code', 'client_id' : self.client_id, 'client_secret' : self.client_secret, 'code' : code, 'redirect_uri' : redirect_URI}
        headers = {'Accept': 'application/json', 'User-Agent':self.SDK_VERSION, 'Content-type':'application/json'}
        uri = self.make_path(self.OAUTH_URL)

        response = self._requests.post(uri, params=urlencode(params), headers=headers)

        if response.status_code == requests.codes.ok:
            response_info = response.json()
            self.access_token = response_info['access_token']
            if 'refresh_token' in response_info:
                self.refresh_token = response_info['refresh_token']
            else:
                self.refresh_token = '' # offline_access not set up
                self.expires_in = response_info['expires_in']

            return self.access_token
        else:
            # response code isn't a 200; raise an exception
            response.raise_for_status()

    def display(self):
        return {'id': self.id}
