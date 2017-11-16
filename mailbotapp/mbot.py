from __future__ import print_function
import httplib2
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import requests
import argparse

class Mbot(object):
    def __init__(self):
        self.ACCESS_TOKEN = "EAAXuNBwZBG9kBAECVP64YldWTKZCJQSYQ5ZBpj1Pm2bWBZAradyU9xYHy7q66Yf4vZAHny0cWJQJNcqQ93ICHHJX7dJSqFUPGwpySZBOQtZCRlKn72JbYqYKPW8H70xdj2BLGS1BQ8DinSggoF2r6OlC3PIEEp8B2oUyLHs7iXHLgZDZD"
#        self.VERIFY_TOKEN = "secret"
        self.SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
 	#self.SCOPES = ['https://mail.google.com/']
        self.CLIENT_SECRETS_FILE = '/var/www/mailbotapp/mailbotapp/client_secret.json'
        self.user_psid = None

    # def reply(self, user_id, msg):
    #     data = {"recipient": {"id": user_id},
    #             "message": {"text": msg}}
    #     resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + self.ACCESS_TOKEN, json=data)
    #     print(resp.content)

    def reply(self, sender_psid, response):
        # Construct the message body
        request_body = {"recipient": {"id": sender_psid},
                        "message": response}
        resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + self.ACCESS_TOKEN,
                             json=request_body)
        print(resp.content)

    def web_authorize(self, user_psid, redirect_uri):
        # Use the client_secret.json file to identify the application requesting
        # authorization. The client ID (from that file) and access scopes are required.
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(self.CLIENT_SECRETS_FILE, self.SCOPES)
        # Indicate where the API server will redirect the user after the user completes
        # the authorization flow. The redirect URI is required.
        flow.redirect_uri = redirect_uri
        # Generate URL for request to Google's OAuth 2.0 server.
        # Use kwargs to set optional request parameters.
        authorization_url, state = flow.authorization_url(
            # Enable offline access so that you can refresh an access token without
            # re-prompting the user for permission. Recommended for web server apps.
            access_type='offline',
            # Enable incremental authorization. Recommended as a best practice.
            include_granted_scopes='true')
        self.user_psid = user_psid
        self.reply(user_psid, self.login_button(authorization_url))
        return state

    def send_login_button(self, user_psid, url):
        self.user_psid = user_psid
        self.reply(user_psid, self.login_button(url))
        return

    def new_authorize(self, user_psid, redirect_uri):
        # Use the client_secret.json file to identify the application requesting
        # authorization. The client ID (from that file) and access scopes are required.
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(self.CLIENT_SECRETS_FILE, self.SCOPES)
        # Indicate where the API server will redirect the user after the user completes
        # the authorization flow. The redirect URI is required.
        flow.redirect_uri = redirect_uri
        # Generate URL for request to Google's OAuth 2.0 server.
        # Use kwargs to set optional request parameters.
        authorization_url, state = flow.authorization_url(
            # Enable offline access so that you can refresh an access token without
            # re-prompting the user for permission. Recommended for web server apps.
            access_type='offline',
            # Enable incremental authorization. Recommended as a best practice.
            include_granted_scopes='true')
        return authorization_url, state

    def oauth2callback(self, state, redirect_uri, authorization_response):
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            self.CLIENT_SECRETS_FILE, scopes=self.SCOPES, state=state)
        flow.redirect_uri = redirect_uri
        # Use the authorization server's response to fetch the OAuth 2.0 tokens.
        flow.fetch_token(authorization_response=authorization_response)
        # Store credentials in the session.
        # ACTION ITEM: In a production app, you likely want to save these
        #              credentials in a persistent database instead.
	self.reply(self.user_psid, {"text": 'Authorization went fine. Thank you!'})
	credentials = flow.credentials
	return Mbot.credentials_to_dict(credentials)

    def access_gmail(self,credentials):	
	GMAIL = build('gmail', 'v1', credentials=credentials, cache_discovery=False)
  
	###connecting to GMAIL###
	threads = GMAIL.users().threads().list(userId='me').execute().get('threads', [])
	#for thread in threads:
	#retrieve only last:
	subjects = []
	for t in range(1):    
            tdata = GMAIL.users().threads().get(userId='me', id=threads[t]['id']).execute()
	    #tdata = GMAIL.users().threads().get(userId='me', id=thread['id']).execute()
	    nmsgs = len(tdata['messages'])

	    if nmsgs > 0:
	        msg = tdata['messages'][0]['payload']
	        subject = ''
	        for header in msg['headers']:
	            if header['name'] == 'Subject':
	                subject = header['value']
	                break
	        if subject:
			subjects.append(subject)
	return subjects
    
    @staticmethod
    def credentials_to_dict(credentials):
        return {'token': credentials.token,
		'refresh_token': credentials.refresh_token,
		'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'scopes': credentials.scopes}

    @staticmethod
    def credentials_from_dict(cred_dict):
	credentials = google.oauth2.credentials.Credentials(cred_dict['token'],refresh_token=cred_dict['refresh_token'],token_uri=cred_dict['token_uri'],client_id=cred_dict['client_id'],client_secret=cred_dict['client_secret'],scopes=cred_dict['scopes']
)
	return credentials

    @staticmethod
    def login_button(url):
        response = \
            {"attachment":
                 {"type": "template",
                  "payload":
                      {"template_type": "generic",
                       "elements":
                           [{"title": "Please login to your Gmail account",
                             "buttons":
                                 [{"type": "web_url",
                                   "url": url,
                                   "title": "Gmail Login",
                                   "webview_height_ratio": "tall",
                                   "messenger_extensions": False,
                                   "webview_share_button": "hide"}]
                             }]
                       }
                  }
             }
        return response
