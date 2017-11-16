from __future__ import print_function
import flask
from .mbot import Mbot
from .forms import ChatForm
import os
# TODO: make it work with https 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = flask.Flask(__name__)

mbot = Mbot()


# @app.route('/')
# def check_server():
#	return 'ok'

@app.route('/', methods=['GET'])
def handle_verification():
    if flask.request.args['hub.verify_token'] == mbot.VERIFY_TOKEN:
        return flask.request.args['hub.challenge']
    else:
        return "Invalid verification token"


@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = flask.request.json
    sender = data['entry'][0]['messaging'][0]['sender']['id']
    #message = data['entry'][0]['messaging'][0]['message']['text']
    # redirect_uri = flask.url_for('oauth2callback', _external=True)
    # state = mbot.web_authorize(sender, redirect_uri)
    # # Store the state so the callback can verify the auth server response.
    # flask.session['state'] = state
    print('sender psid:', sender)
    #print(message)
    auth_url = flask.url_for('authorize', user_psid=sender, _external=True)
    mbot.send_login_button(sender, auth_url)
    chat_url = flask.url_for('chat', _external=True)
    mbot.send_login_button(sender, chat_url)
    #mbot.reply(sender, message)
    # mbot.callSendAPI(sender, createLoginButton("https://www.google.com"))
    return "ok"


@app.route('/authorize/<int:user_psid>')
def authorize(user_psid):
    redirect_uri = flask.url_for('oauth2callback', _external=True)
    authorization_url, state = mbot.new_authorize(user_psid, redirect_uri)
    # Store the state so the callback can verify the auth server response.
    flask.session['state'] = state
    return flask.redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = flask.session['state']
    redirect_uri = flask.url_for('oauth2callback', _external=True)
    authorization_response = flask.request.url
    credentials = mbot.oauth2callback(state, redirect_uri, authorization_response)
    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    #
    return redirect_uri


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    form = ChatForm()
    return flask.render_template('chat.html', form=form)


if __name__ == "__main__":
    app.run()
