from __future__ import print_function
import httplib2
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import requests
import argparse
import json
from database.database import add_user, add_reply, get_unsent_emails, update_email_stats, user_exists, get_FB_id, get_email, add_email, get_old_emails

#add_reply(('olg@gmail.com', 87, subject, 'Adil', reply_text,'august 11', 0))
class Mbot(object):
    def __init__(self):
        self.ACCESS_TOKEN = "EAAXuNBwZBG9kBAECVP64YldWTKZCJQSYQ5ZBpj1Pm2bWBZAradyU9xYHy7q66Yf4vZAHny0cWJQJNcqQ93ICHHJX7dJSqFUPGwpySZBOQtZCRlKn72JbYqYKPW8H70xdj2BLGS1BQ8DinSggoF2r6OlC3PIEEp8B2oUyLHs7iXHLgZDZD"
        self.VERIFY_TOKEN = "secret"
        #self.SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
        self.SCOPES = ['https://mail.google.com/']
        self.CLIENT_SECRETS_FILE = '/var/www/mailbotapp/mailbotapp/client_secret.json'
        self.base_url = 'https://a0ddbefd.ngrok.io/'

    def send_text(self, user_psid, text):
        self.send_message(user_psid, {"text": text})
        return

    def send_message(self, user_psid, response):
        # Construct the message body
        request_body = {"recipient": {"id": user_psid},
                        "message": response}
        resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + self.ACCESS_TOKEN,
                             json=request_body)
        print(resp.content)
        return

    def send_email_as_message(self, user_psid, email_id, sender_name, subject):
        chat_url = self.base_url + 'chat/'+str(user_psid)+'/'+str(email_id)
        new_email_url = self.base_url + 'newEmail/' + str(user_psid)
        message = Mbot.message_with_button2(new_email_url, 'New Email', chat_url, 'Open and Reply', sender_name+": "+subject)
        self.send_message(user_psid, message)
        return

    def send_unsent_emails(self):
		data = get_unsent_emails()
		for row in data:
		    email_id = row[0]
		    user_id = row[1]
		    fb_id = get_FB_id(user_id) # TODO: get fb_id from user id
		    print(fb_id)
		    #fb_id = 1438669066252571
		    subject = row[3]
		    sender_name = row[4]
		    self.send_email_as_message(fb_id, email_id, sender_name, subject)
		update_email_stats()
		return

    def get_email(self, email_id):
		print('id:',email_id)
		email = get_email(email_id)
		print('email:', email)
		sender_name = email[4]
		subject = email[3]
		text = email[5]
		return sender_name, subject, text

    def send_login_button(self, user_psid, url):
        message = self.message_with_button(url, url_title='Gmail Login',
                                          message_title='Please login to your Gmail account',
                                          message_subtitle='Tap the button')
        self.send_message(user_psid, message)
        return

    def check_authorized(self, user_psid):
        return user_exists(user_psid)

    def authorize(self, redirect_uri):
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

    def oauth2callback(self, user_psid, state, redirect_uri, authorization_response):
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            self.CLIENT_SECRETS_FILE, scopes=self.SCOPES, state=state)
        flow.redirect_uri = redirect_uri
        # Use the authorization server's response to fetch the OAuth 2.0 tokens.
        flow.fetch_token(authorization_response=authorization_response)
        # Store credentials in the session.
        # ACTION ITEM: In a production app, you likely want to save these
        #              credentials in a persistent database instead.
        self.send_message(user_psid, {"text": 'Authorization went fine. Thank you!'})
        credentials = Mbot.credentials_to_dict(flow.credentials)
        self.save_credentials(user_psid, credentials)
        return credentials

    def create_email(self, user_psid, recipient_email, subject, body):
        return

    def create_reply_email(self, reply):
        add_reply(reply)
        return 

    def save_credentials(self, user_psid, credentials):
        # TODO: save credentials in database
        add_user(user_psid, json.dumps(credentials))
        return
    
    def get_user_id_and_sender_id_from_email_id(self, email_id):
        email = get_email(email_id)
        user_id = email[1]
        sender_id = email[2]
        return user_id, sender_id    
    #print(get_user_id_and_sender_id_from_email_id(1))
    def old_emails(self, user_id, sender_id):
        return get_old_emails(user_id, sender_id)

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
        credentials = google.oauth2.credentials.Credentials(cred_dict['token'],
                                                            refresh_token=cred_dict['refresh_token'],
                                                            token_uri=cred_dict['token_uri'],
                                                            client_id=cred_dict['client_id'],
                                                            client_secret=cred_dict['client_secret'],
                                                            scopes=cred_dict['scopes'])
        return credentials

    @staticmethod
    def message_with_button(url, url_title, message_title, message_subtitle):
        response = \
            {"attachment":
                 {"type": "template",
                  "payload":
                      {"template_type": "generic",
                       "elements":
                           [{"title": message_title,
                             "subtitle": message_subtitle,
                             "buttons":
                                 [{"type": "web_url",
                                   "url": url,
                                   "title": url_title,
                                   "webview_height_ratio": "tall",
                                   "messenger_extensions": False,
                                   "webview_share_button": "hide"}]
                             }]
                       }
                  }
             }
        return response

    @staticmethod
    def message_with_button2(url1, url_title1, url2, url_title2, message_title):
        response = \
            {"attachment":
                 {"type": "template",
                  "payload":
                      {"template_type": "generic",
                       "elements":
                           [{"title": message_title,
                             "buttons":
                                 [{"type": "web_url",
                                   "url": url1,
                                   "title": url_title1,
                                   "webview_height_ratio": "tall",
                                   "messenger_extensions": False,
                                   "webview_share_button": "hide"},
                                 {"type": "web_url",
                                  "url": url2,
                                  "title": url_title2,
                                  "webview_height_ratio": "tall",
                                  "messenger_extensions": False,
                                  "webview_share_button": "hide"}]
                             }]
                       }
                  }
             }
        return response
