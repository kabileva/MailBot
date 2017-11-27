from __future__ import print_function
import httplib2
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import requests
import argparse
import json
from database.database import add_user, get_user_photo, get_user_id, get_unsent_emails, update_email_stats, user_exists, get_FB_id, get_email, add_email, get_old_emails

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
    def get_user_photo(self, user_id):
        photo = get_user_photo(user_id)
        return photo 
    def send_message(self, user_psid, response):
        # Construct the message body
        request_body = {"recipient": {"id": user_psid},
                        "message": response}
        resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + self.ACCESS_TOKEN,
                             json=request_body)
        print(resp.content)
        return

    def send_email_as_message(self, user_psid, email_id, sender_name, subject):
        chat_url = self.base_url + 'chat/'+str(user_psid)+'/'+str(email_id) + '#email' + str(email_id)
        new_email_url = self.base_url + 'newEmail/' + str(user_psid)
        message = Mbot.message_with_button2(new_email_url, 'New Email', chat_url, 'Open and Reply', sender_name+": "+subject)
        self.send_message(user_psid, message)
        return

    def send_welcome(self, user_psid):
        new_email_url = self.base_url + 'newEmail/' + str(user_psid)
        message = Mbot.message_with_button(new_email_url, 'New Email', 'Authorization went fine. Thank you! You can compose new email using this button. Once you receive an email, you will see it here.')
        self.send_message(user_psid, message)
        return

    def send_instructions(self, user_psid):
        new_email_url = self.base_url + 'newEmail/' + str(user_psid)
        message = Mbot.message_with_button(new_email_url, 'New Email', "You can compose new email using this button. Once you receive an email, you will see it here. You can search for email conversation by typing 'search <email or name>'")
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
		#print('id:',email_id)
		email = get_email(email_id)
		#print('email:', email)
		#sender_name = email[4]
		#subject = email[3]
		#text = email[5]
		return email

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
        self.send_welcome(user_psid)
        credentials = Mbot.credentials_to_dict(flow.credentials)
        self.save_credentials(user_psid, credentials)
        return credentials

    def create_email(self, recipient_id, sender_id, subject, sender_name, text, date_time, sent, photo, sent_or_received, attachment):
        add_email((recipient_id, sender_id, subject, sender_name, text, date_time, sent, photo, sent_or_received, attachment))

 #   def create_reply_email(self, reply):
  #      add_reply(reply)
   #     return 
    def get_user_id(self, FB_id):
       user_id = get_user_id(FB_id)
       return user_id
 
    def save_credentials(self, user_psid, credentials):
        # TODO: save credentials in database
        add_user(user_psid, json.dumps(credentials), 'https://lh3.googleusercontent.com/-XMt0yYeRLJc/AAAAAAAAAAI/AAAAAAAAAAA/txEeL9uI8Vo/s64-c/116749323011652222288.jpg')
        return
    
    def get_user_id_and_sender_id_from_email_id(self, email_id):
        email = get_email(email_id)
        user_id = email[1]
        sender_id = email[2]
        return user_id, sender_id    
    #print(get_user_id_and_sender_id_from_email_id(1))
    def get_old_emails(self, user_id, sender_id):
        old_emails =  get_old_emails(user_id, sender_id)
        #print(len(old_emails))
        html = []
        for i in range(0, len(old_emails)):
            if (old_emails[i][9] == -1):
                #print('was sent to us')
                html.append("<li id='email{em_id}' class='left clearfix'> <span class='chat-img pull-left'><img src={photo} alt='User Avatar' width='50' height='50' class='img-circle' /></span><div class='chat-body clearfix'><div class='header'><strong class='primary-font'>{name}</strong> <small class='pull-right text-muted'><span class='glyphicon glyphicon-time'></span>{date}</small></div>".format(em_id=old_emails[i][0], photo = old_emails[i][8], name = old_emails[i][4], date = old_emails[i][6]))
            else: 
                html.append("<li id='email{em_id}' class='right clearfix'> <span class='chat-img pull-right'><img src={photo} alt='User Avatar' width='50' height='50' class='img-circle' /></span><div class='chat-body clearfix'><div class='header'><small class='text-muted'><span class='glyphicon glyphicon-time'></span>{date}</small><strong class='pull-right primary-font'>{name}</strong></div>".format(em_id=old_emails[i][0], photo = old_emails[i][8], name = old_emails[i][4], date = old_emails[i][6]))
            html.append("<p>Subject: {subject}</p>".format(subject=old_emails[i][3]))
            html.append("<p>{text}</p>".format(text=old_emails[i][5]))
            if old_emails[i][10] is not None:
                # TODO: check for possible bugs
                atts = old_emails[i][10].split(';')
                urls = []
                for att in atts:
                    url = self.base_url + 'attachment/' + att.strip()
                    name = att.split('_')[-1]
                    html.append("<a href='{link}' download>{name}</a>".format(link=url, name=name))
            html.append("</div></li>")
        return '\n'.join(html)

    
            
    
    # given an email id it returns the whole chain of emails in the current conversation. Returns an array of emails
    def get_conversation_history(email_id):
        conversation_history = []
        this_email = get_email(email_id)    
        next_email_id = this_email[9]  #= email_prev_email_id
        conversation_history.append(this_email)
        while (next_email_id != -1):
            this_email = get_email(next_email_id)
            conversation_history.append(this_email)
            next_email_id = this_email[9]
       # return conversation_history
       # just for test:
        texts = []
        for email in conversation_history:
            texts.append(email[5])
        result = '\n'.join(texts)
        return result

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
    def message_with_button(url, url_title, text):
        response = \
            {"attachment":
                 {"type": "template",
                  "payload":
                      {"template_type": "button",
                       "text": text,
                       "buttons":
                                 [{"type": "web_url",
                                   "url": url,
                                   "title": url_title,
                                   "webview_height_ratio": "tall",
                                   "messenger_extensions": False,
                                   "webview_share_button": "hide"}]
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
