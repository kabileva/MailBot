from flask_wtf import Form
from wtforms import TextField

class ChatForm(Form):
	email = TextField("Your email")
