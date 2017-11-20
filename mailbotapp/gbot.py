from __future__ import print_function
import httplib2
from googleapiclient.discovery import build
#from database.database import *
import base64
import re
from bs4 import BeautifulSoup
if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        from mbot import Mbot
    else:
        from .mbot import Mbot
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import time
import json
class Gbot(object):
	def __init__(self):
		self.gmail = None
	
	def access_gmail(self,credentials):
		self.gmail = build('gmail', 'v1', credentials=credentials, cache_discovery=False)
	
	def get_emails(self, after_time):
		query = 'is:unread AND after:%d'%(after_time)
		threads = self.gmail.users().messages().list(userId='me', q = query).execute()
		emails = []
		if not 'messages' in threads:
			return emails, time.time()
		for email in threads['messages']:
			msg_id = email['id']
			email_det = self.gmail.users().messages().get(userId='me',id=msg_id).execute()	
			emails.append(email_det)
		return emails, time.time()

	def get_subject(self,email):
		for header in email['payload']['headers']:
			if header['name']=='Subject':
				return str(header['value'])
	def get_sender(self,email):
		for header in email['payload']['headers']:
			if header['name']=='From':
				tmp = header['value'].split('<')
				#print(tmp)
				name = tmp[0]
				print(str(name))
				print(type(str(name)))
				email = tmp[1].split('>')[0]
                return str(name), str(email)

	def get_body(self, email):
		mssg_parts = email['payload']['parts'] # fetching the message parts
		part_one  = mssg_parts[0] # fetching first element of the part 
		part_body = part_one['body'] # fetching body of the message
		part_data = part_body['data'] # fetching data from the body
		clean_one = part_data.replace("-","+") # decoding from Base64 to UTF-8
		clean_one = clean_one.replace("_","/") # decoding from Base64 to UTF-8
		clean_two = base64.b64decode (bytes(clean_one)) # decoding from Base64 to UTF-8
		print(clean_two)
#		soup = BeautifulSoup(clean_two , "lxml" )
#		mssg_body = soup.body()
#		print(type(mssg_body[0]))
#		return mssg_body[0]
		return str(clean_two)
		# mssg_body is a readible form of message body
		# depending on the end user's requirements, it can be further cleaned 
		# using regex, beautiful soup, or any other method
