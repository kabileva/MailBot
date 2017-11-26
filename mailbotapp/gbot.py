from __future__ import print_function
import httplib2
from email.MIMEMultipart import MIMEMultipart
import os
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
from googleapiclient.discovery import build
from database.database import *
import base64
import urllib
import re
from bs4 import BeautifulSoup
from mbot import Mbot
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
        print(self.gmail) 
    def get_emails(self, after_time):
        query = 'is:unread AND after:%d'%(after_time)
        threads = self.gmail.users().messages().list(userId='me', q = query).execute()
        
        emails = []
        if not 'messages' in threads:
            return emails, time.time()
        while 'nextPageToken' in threads:
            page_token = threads['nextPageToken']
            threads.extend(self.gmail.users().messages().list(userId='me', q = query, pageToken = page_token).execute())
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
                name = tmp[0].strip()
                email = tmp[1].split('>')[0].strip()
                return str(name), str(email)

    def get_body(self, email):
        
        print(email)
        mssg_parts = email['payload']['parts'] # fetching the message parts
        withAtt=False
        if email['payload']['mimeType']=='multipart/mixed':
            withAtt = True
        text = ''
        for part in mssg_parts:
            if 'value'=='text/plain':
                part_one=part
                part_body = part_one['body'] # fetching body of the message
                part_data = part_body['data'] # fetching data from the body
                clean_one = part_data.replace("-","+") # decoding from Base64 to UTF-8
                clean_one = clean_one.replace("_","/") # decoding from Base64 to UTF-8
                clean_two = base64.b64decode (bytes(clean_one)) # decoding from Base64 to UTF-8
                text = str(clean_two), withAtt
        return text,withAtt
    
    #OUTPUT:[(file_name, byte_data),(..)...]       
    def get_attachments(self,email):
        msg_id = email['id']
        
        msg = self.gmail.users().messages().get(userId='me', id = msg_id).execute()
        files_data = []
        for part in msg['payload']['parts']:
            newvar = part['body']
            if 'attachmentId' in newvar:      
                att_id = newvar['attachmentId']
                att = self.gmail.users().messages().attachments().get(userId='me', messageId=msg_id, id=att_id).execute()
                data = att['data']
                file_data = part['filename'],base64.urlsafe_b64decode(data.encode('UTF-8'))
                print(part['filename'])

                files_data.append(file_data)
        return files_data
    def data_to_file(self,file_data):
        name = file_data[0]
        data = file_data[1]
        
    def get_photo(self, email_addr):
        url = 'http://picasaweb.google.com/data/entry/api/user/'+email_addr+'?alt=json'
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        photo = data['entry']['gphoto$thumbnail']['$t']
        return str(photo)

    def send_email(self,sender_psid, receiver_email,subject, email_text, attachment=None):
        mbot = Mbot()
        sender = get_user_id(sender_psid)
        sender_token = mbot.credentials_from_dict(json.loads(sender[2]))
        self.access_gmail(sender_token)
        #message = MIMEText(email_text)
        message = MIMEMultipart()
        message['to']= receiver_email
        message['subject'] = subject
        message.attach(MIMEText(email_text, 'plain'))
        #attachment = '/var/www/mailbotapp/mailbotapp/token.json'
        if not attachment==None:
            att_name = os.path.split(attachment)[1]
            att_file = open(attachment, 'rb')
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((att_file).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % att_name)
        #part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            message.attach(part)
        email = {'raw': base64.urlsafe_b64encode(message.as_string())}
        self.gmail.users().messages().send(userId='me', body=email).execute()      
