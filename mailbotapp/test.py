if __name__ == '__main__':
	if __package__ is None:
		import sys
		from os import path
		sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
		from mbot import Mbot
		from gbot import Gbot
	else:
		from .mbot import Mbot	
		from .gbot import Gbot
gbot = Gbot()
mbot = Mbot()
#psid = 835227646602037
import json
import time
from database.database import *
sys.setdefaultencoding('utf-8')

users = get_users()
users_list = []
for user in users:
	tmp = []
	tmp.append(user[0])
	tmp.append(user[1])
	tmp.append(user[2])
	tmp.append(time.time())
	#[user_id,psid,token,time]
	users_list.append(tmp)
#after_time = time.time()

while True:
#	print('checking after %d'%(after_time))
#	print('checking on %d'%(time.time()))
	for user in users_list:
		user_id = user[0]
		psid = user[1]
		creds = mbot.credentials_from_dict(json.loads(user[2]))
	#	print(creds)
		gmail = gbot.access_gmail(creds)
		emails_raw,user[3] = gbot.get_emails(user[3])
	#	subjects,user[2] = access_gmail(creds,user[2])
		for email_raw in emails_raw:
			print(email_raw)
			subject = gbot.get_subject(email_raw)
			print(subject)
			sender_name, sender_email = gbot.get_sender(email_raw)
			print(sender_name, sender_email)
			body = gbot.get_body(email_raw)
			print(body)
			email = (user_id,sender_email, subject, sender_name, body, '2017-10-29 17:45:40', 0)
			print(email)
			add_email(email)
			
			#mbot.send_message(psid, {"text":subject})
	mbot.send_unsent_emails()
