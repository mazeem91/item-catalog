import json
import requests
import httplib2
from oauth2client.client import FlowExchangeError
from oauth2client.client import flow_from_clientsecrets


class GoolgleLogin():
    def Connect(self, code):

        # code = request.data
        try:
            # Upgrade the authorization code into a credentials object
            authflow = flow_from_clientsecrets('client_secrets.json', scope='')
            authflow.redirect_uri = 'postmessage'
            self.credentials = authflow.step2_exchange(code)
        except FlowExchangeError:
            return 'Failed to upgrade the authorization code.', 401

        # Check that the access token is valid.
        access_token = self.credentials.access_token
        url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
               % access_token)
        h = httplib2.Http()
        result = json.loads(h.request(url, 'GET')[1])
        # If there was an error in the access token info, abort.
        if result.get('error'):
            return result.get('error'), 500

        # Verify that the access token is used for the intended user.
        gplus_id = self.credentials.id_token['sub']
        if result['user_id'] != gplus_id:
            return "Token's user ID doesn't match given user ID.", 401

        # Verify that the access token is valid for this app.
        client_id = json.loads(
            open('client_secrets.json', 'r').read())['web']['client_id']
        if result['issued_to'] != client_id:
            return "Token's client ID does not match app's.", 401

        return self.credentials, 200

        # stored_credentials = login_session.get('access_token')
        # stored_gplus_id = login_session.get('gplus_id')
        # if stored_credentials and gplus_id == stored_gplus_id:
        #     return 'user is already connected.', 200

        # login_session['access_token'] = credentials.access_token
        # login_session['gplus_id'] = gplus_id

    def GetInfo():
        # Get user info
        userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        params = {'access_token': self.credentials.access_token, 'alt': 'json'}
        data = requests.get(userinfo_url, params=params).json()
        return data
        # login_session['username'] = data['name']
        # login_session['picture'] = data['picture']
        # login_session['email'] = data['email']
