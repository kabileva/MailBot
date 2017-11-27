from __future__ import print_function
import flask
from .mbot import Mbot
from .gbot import Gbot
from werkzeug.utils import secure_filename
from .forms import ChatForm, NewEmailForm
import os
import time
# TODO: make it work with https 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = flask.Flask(__name__)

mbot = Mbot()
gbot = Gbot()


# @app.route('/')
# def check_server():
#   return 'ok'

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
    messagingArray = data['entry'][0]['messaging'][0]
    #print(messagingArray)
    if messagingArray.has_key('postback'):
        if messagingArray['postback']['payload'] == 'GET_STARTED_PAYLOAD':
            mbot.send_text(sender, 'Hello there!')
    if not mbot.check_authorized(sender):
        auth_url = flask.url_for('authorize', user_psid=sender, _external=True)
        mbot.send_login_button(sender, auth_url)
#    print('sender psid:', sender)
    # message = data['entry'][0]['messaging'][0]['message']['text']
    # print(message)
    chat_url = flask.url_for('chat', user_psid=sender, email_id=0, _external=True)
    mbot.send_email_as_message(sender, 6, 'Bill Gates', 'I need your help')
    #mbot.create_dummy_email(sender)
    mbot.send_unsent_emails()
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
    # TODO: make it secure
    form = ChatForm()
    email = mbot.get_email(email_id)
    user_id, sender_id = mbot.get_user_id_and_sender_id_from_email_id(email_id)
    conv_body = mbot.get_old_emails(user_id, sender_id)
    if flask.request.method == 'POST':
        if form.validate() is False:
            flask.flash('All fields are required.')
            return flask.render_template('reply.html', form=form, conv_body=conv_body, action_url=flask.url_for('chat', user_psid=user_psid,
                                                                                   email_id=email_id, _external=True))
        else:
            attach = form.attachment.data
            filename = None
            full_filename = None
            print(attach)
            if attach is not None:
                filename = secure_filename(attach.filename)
                filename = str(user_psid) + '_' + str(time.time()) + '_' + filename
                full_filename = '/var/www/mailbotapp/uploads/' + filename
                attach.save(full_filename)
            user_photo = mbot.get_user_photo(email[1])
            mbot.create_email(email[1], email[2], email[3], email[4], form.message.data, email[6], 1, user_photo,  1, filename)
            gbot.send_email(user_psid, email[2], email[3], form.message.data, full_filename)
            #reply_text = form.message.data
            #mbot.create_email()
            #print(reply_text)
            #mbot.create_reply_email(('olg@gmail.com', 87, subject, 'Adil', reply_text,'august 11', 0))
            return flask.render_template('reply.html', success=True, _external=True)
    #lst = mbot.get_email(email_id)
    #print('get_email returns:',lst)
    #get old emails from the given sender
    #user_id, sender_id = mbot.get_user_id_and_sender_id_from_email_id(email_id)
    #emails_old = mbot.old_emails(user_id, sender_id)
    return flask.render_template('reply.html', form=form, conv_body=conv_body, action_url=flask.url_for('chat', user_psid=user_psid,
                                                                                 email_id=email_id, _external=True))


@app.route('/newEmail/<int:user_psid>', methods=['GET', 'POST'])
def newEmail(user_psid):
    form = NewEmailForm()
    if flask.request.method == 'POST':
        if form.validate() is False:
            flask.flash('All fields are required.')
            return flask.render_template('new_email.html', form=form,
                                         action_url=flask.url_for('newEmail', user_psid=user_psid, _external=True))
        else:
            # TODO: create email
            attach = form.attachment.data
            filename = None
          #  print(attach)
           # print(user_psid)
            if attach is not None:
                filename = secure_filename(attach.filename)
                filename = str(user_psid) + '_' + str(time.time()) + '_' + filename
                full_filename = '/var/www/mailbotapp/uploads/' + '_' + filename
                attach.save(full_filename)
            user_id = mbot.get_user_id(user_psid)
          #  print(user_id)
            user_photo = mbot.get_user_photo(user_id)
            mbot.create_email(user_id, form.email.data, form.subject.data, 'email', form.message.data, '2017-10-29 17:45:40', 1, user_photo, 1, filename)
            
            gbot.send_email(user_psid, form.email.data, form.subject.data, form.message.data, full_filename)
            return flask.render_template('new_email.html', success=True, _external=True)
    return flask.render_template('new_email.html', form=form,
                                 action_url=flask.url_for('newEmail', user_psid=user_psid, _external=True))

@app.route('/attachment/<path:path>', methods=['GET'])
def get_attachment(path):
    return flask.send_from_directory('/var/www/mailbotapp/uploads/', path, as_attachment=True)

if __name__ == "__main__":
    #print(get_user_id_and_sender_id_from_email_id(1))
    app.run()

