from __future__ import print_function
import httplib2
from googleapiclient.discovery import build
from database.database import *
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
mbot = Mbot()
#Kate's psid: sender psid: 835227646602037
psid = 835227646602037
import json
cred_dict = json.load(open('/var/www/mailbotapp/mailbotapp/token.json'))
cred_dict3 = {
  "client_id": "931653727468-ncf4n4k90t8u0et2pj9808gn9h8rvkal.apps.googleusercontent.com", 
  "client_secret": "gKWtUvSK14mA6D9PmPDzXIlD", 
  "refresh_token": None, 
  "scopes": "https://www.googleapis.com/auth/gmail.readonly", 
  "token": "ya29.GlwEBfZKpyoD_k910Vbx5iDpPlTlcIa3VotFSOPPMBi2Rjd5ooYgNUUcQ7yqZj1PSzQpjSa1XbK6_ZG2zq16RCMo8e44v7s4CP70P3s0QKUM8m82cklYJ-u1363gJw", 
  "token_uri": "https://accounts.google.com/o/oauth2/token"
}
count = 0
#if(count<1):
#	add_user(psid,json.dumps(cred_dict))
#	count+=1
n = 0
def access_gmail(credentials, after_time):
	GMAIL = build('gmail', 'v1', credentials=credentials, cache_discovery=False)

        query = 'is:unread AND after:%d'%(after_time)
	threads = GMAIL.users().threads().list(userId='me', q = query).execute()
        subjects = []
	print(threads)
	if not 'threads' in threads:
            return subjects, time.time()
	print(threads['threads'])
        for thread in threads['threads']:
	    print(thread['snippet'])
	    subjects.append(thread['snippet'])
            time_checked = time.time()
        return subjects, time_checked

creds = mbot.credentials_from_dict(cred_dict)
after_time = time.time()
while True:
	print('checking after %d'%(after_time))
	print('checking on %d'%(time.time()))
	subjects,after_time = access_gmail(creds,after_time)
	for subject in subjects:
		mbot.reply(psid, {"text":subject})
		print('sent on %d'%(time.time()))


