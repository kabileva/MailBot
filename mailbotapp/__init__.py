from __future__ import print_function

from flask import Flask, request

import httplib2
import os

import google.oauth2.credentials
import google_auth_oauthlib.flow

# Not sure if we need those, but I'll just keep them for a while
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import requests
from httplib2 import Http
from oauth2client import file, client, tools

app = Flask(__name__)

ACCESS_TOKEN = "EAAXuNBwZBG9kBAECVP64YldWTKZCJQSYQ5ZBpj1Pm2bWBZAradyU9xYHy7q66Yf4vZAHny0cWJQJNcqQ93ICHHJX7dJSqFUPGwpySZBOQtZCRlKn72JbYqYKPW8H70xdj2BLGS1BQ8DinSggoF2r6OlC3PIEEp8B2oUyLHs7iXHLgZDZD"
VERIFY_TOKEN = "secret"

def reply(user_id, msg):
	data = {"recipient": {"id": user_id},
		"message": {"text": msg}}
	resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
	print(resp.content)
def callSendAPI(sender_psid, response):
	# Construct the message body
	request_body = {"recipient": {"id": sender_psid},
			"message": response}
	resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=request_body)
        print(resp.content)
def createLoginButton(url):
	response = {"attachment": {"type": "template",
				   "payload": {"template_type": "generic",
					       "elements": [{"title": "Please login to your Gmail account",
							     "subtitle": "Tap the button",
							     "buttons": [{"type": "web_url",
									 "url": url,
									 "title": "Gmail Login",
									 "webview_height_ratio": "tall",
									 "messenger_extensions": False,
									 "webview_share_button": "hide"}]}]}}}
	return response
def web_authorize(user_psid):
	SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
	CLIENT_SECRETS_FILE = '/var/www/mailbotapp/mailbotapp/client_secret.json'
	# Use the client_secret.json file to identify the application requesting
	# authorization. The client ID (from that file) and access scopes are required.
	flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
	# Indicate where the API server will redirect the user after the user completes
	# the authorization flow. The redirect URI is required.
	flow.redirect_uri = 'http://localhost:8080'
	# Generate URL for request to Google's OAuth 2.0 server.
	# Use kwargs to set optional request parameters.
	authorization_url, state = flow.authorization_url(
    		# Enable offline access so that you can refresh an access token without
    		# re-prompting the user for permission. Recommended for web server apps.
    		access_type='offline',
    		# Enable incremental authorization. Recommended as a best practice.
    		include_granted_scopes='true')
	callSendAPI(user_psid, createLoginButton(authorization_url))
def authorize():
	SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
	store = file.Storage('/var/www/mailbotapp/mailbotapp/storage.json')
	creds = store.get()
	if not creds or creds.invalid:
	    flow = client.flow_from_clientsecrets('/var/www/mailbotapp/mailbotapp/client_secret.json', SCOPES)
	    creds = tools.run_flow(flow, store)
	GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))
	
@app.route('/', methods=['GET'])
def handle_verification():
	if request.args['hub.verify_token'] == VERIFY_TOKEN:
		return request.args['hub.challenge']
	else:
		return "Invalid verification token"

@app.route('/', methods=['POST'])
def handle_incoming_messages():
	data = request.json
	sender = data['entry'][0]['messaging'][0]['sender']['id']
	message = data['entry'][0]['messaging'][0]['message']['text']

	web_authorize(sender)
	#reply(sender, message)
	#callSendAPI(sender, createLoginButton("https://www.google.com"))	
	return "ok"

if __name__ == "__main__":
	app.run()
