from flask_wtf import Form
from wtforms import TextAreaField, SubmitField, TextField
from wtforms.validators import DataRequired, Email


class ChatForm(Form):
    message = TextAreaField("Message", validators=[DataRequired("Please enter a message.")])
    submit = SubmitField("Send")


class NewEmailForm(Form):
    email = TextField("To", validators=[DataRequired("Please enter recipient's email address."),
                                        Email("Please enter a valid email.")])
    subject = TextField("Subject", validators=[DataRequired("Please enter a subject.")])
    message = TextAreaField("Message", validators=[DataRequired("Please enter a message.")])
    submit = SubmitField("Send")
