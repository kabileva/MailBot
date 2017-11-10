from __future__ import print_function

from flask import Flask, request

import httplib2
import os
import requests
from httplib2 import Http
from .mbot import Mbot

app = Flask(__name__)

mbot = Mbot()

#@app.route('/')
#def check_server():
#	return 'ok'
	
@app.route('/', methods=['GET'])
def handle_verification():
	if request.args['hub.verify_token'] == mbot.VERIFY_TOKEN:
		return request.args['hub.challenge']
	else:
		return "Invalid verification token"

@app.route('/', methods=['POST'])
def handle_incoming_messages():
	data = request.json
	sender = data['entry'][0]['messaging'][0]['sender']['id']
	message = data['entry'][0]['messaging'][0]['message']['text']

	mbot.web_authorize(sender)
	#mbot.reply(sender, message)
	#mbot.callSendAPI(sender, createLoginButton("https://www.google.com"))	
	return "ok"

if __name__ == "__main__":
	app.run()
