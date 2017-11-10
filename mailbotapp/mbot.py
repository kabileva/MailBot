import google.oauth2.credentials
import google_auth_oauthlib.flow
import requests

class Mbot(object):
	def __init__(self):
		self.ACCESS_TOKEN = "EAAXuNBwZBG9kBAECVP64YldWTKZCJQSYQ5ZBpj1Pm2bWBZAradyU9xYHy7q66Yf4vZAHny0cWJQJNcqQ93ICHHJX7dJSqFUPGwpySZBOQtZCRlKn72JbYqYKPW8H70xdj2BLGS1BQ8DinSggoF2r6OlC3PIEEp8B2oUyLHs7iXHLgZDZD"
		self.VERIFY_TOKEN = "secret"
	def reply(self, user_id, msg):
        	data = {"recipient": {"id": user_id},
			"message": {"text": msg}}
        	resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" +self.ACCESS_TOKEN, json=data)
        	print(resp.content)
	def callSendAPI(self, sender_psid, response):
        	# Construct the message body
        	request_body = {"recipient": {"id": sender_psid},
                        	"message": response}
        	resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + self.ACCESS_TOKEN, json=request_body)
        	print(resp.content)
	def createLoginButton(self, url):
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
	def web_authorize(self, user_psid):
        	SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
        	CLIENT_SECRETS_FILE = '/var/www/mailbotapp/mailbotapp/client_secret.json'
        	# Use the client_secret.json file to identify the application requesting
        	# authorization. The client ID (from that file) and access scopes are required.
        	flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
        	# Indicate where the API server will redirect the user after the user completes
        	# the authorization flow. The redirect URI is required.
        	flow.redirect_uri = 'http://localhost:6680'
        	# Generate URL for request to Google's OAuth 2.0 server.
        	# Use kwargs to set optional request parameters.
        	authorization_url, state = flow.authorization_url(
                	# Enable offline access so that you can refresh an access token without
                	# re-prompting the user for permission. Recommended for web server apps.
                	access_type='offline',
                	# Enable incremental authorization. Recommended as a best practice.
                	include_granted_scopes='true')
        	self.callSendAPI(user_psid, self.createLoginButton(authorization_url))
	



