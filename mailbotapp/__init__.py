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
    if not mbot.check_authorized(sender):
        auth_url = flask.url_for('authorize', user_psid=sender, _external=True)
        mbot.send_login_button(sender, auth_url)
    print('sender psid:', sender)
    # message = data['entry'][0]['messaging'][0]['message']['text']
    # print(message)
    chat_url = flask.url_for('chat', user_psid=sender, email_id=0, _external=True)
    mbot.send_email_as_message(sender, 0, 'Bill Gates', 'I need your help')
    return "ok"


@app.route('/authorize/<int:user_psid>')
def authorize(user_psid):
    redirect_uri = flask.url_for('oauth2callback', _external=True)
    authorization_url, state = mbot.authorize(redirect_uri)
    # Store the state so the callback can verify the auth server response.
    flask.session['state'] = state
    flask.session['user_psid'] = user_psid
    return flask.redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = flask.session['state']
    user_psid = flask.session['user_psid']
    redirect_uri = flask.url_for('oauth2callback', _external=True)
    authorization_response = flask.request.url
    credentials = mbot.oauth2callback(user_psid, state, redirect_uri, authorization_response)
    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    #
    return flask.jsonify(credentials)


@app.route('/chat/<int:user_psid>/<int:email_id>', methods=['GET', 'POST'])
def chat(user_psid, email_id):
    form = ChatForm()
    return flask.render_template('chat.html', form=form, sender_name="Bill Gates", subject="I need your help", email_text="I'm short on cash. Can you lend me 500k?", action_url=flask.url_for('chat', user_psid=user_psid, email_id=email_id, _external=True))


if __name__ == "__main__":
    app.run()
