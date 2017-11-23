from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email


class ChatForm(Form):
	#email = StringField('Email', validators=[DataRequired(), Email()])
	#password = PasswordField('Password', validators=[DataRequired()]) 
	message = TextAreaField("Message", validators=[DataRequired()])
	submit = SubmitField("Send")


class NewEmailForm(Form):
	subject = TextAreaField("Subject")
