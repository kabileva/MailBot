
if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        from mbot import Mbot
    else:
        from .mbot import Mbot
import time
mbot = Mbot()
#Kate's psid: sender psid: 835227646602037
psid = 835227646602037
n = 0
token = {
  "client_id": "931653727468-ncf4n4k90t8u0et2pj9808gn9h8rvkal.apps.googleusercontent.com", 
  "client_secret": "gKWtUvSK14mA6D9PmPDzXIlD", 
  "refresh_token": "", 
  "scopes": [
    "https://www.googleapis.com/auth/gmail.readonly"
  ], 
  "token": "ya29.GlwCBdn5YuQ_Rav3PLGZOH4T8HjNtB_sQJgGy56-rFg55mxB4V1doy3CRKjRjemKK244OlUtfXwlCcOdUQ_a1TuCivE7jMFYnl_ZEnHZ1X14FsP-rw_QgmRDrAmyMw", 
  "token_uri": "https://accounts.google.com/o/oauth2/token"
}
import oauth2
client_id = token['client_id']
client_secret = token['client_secret']
refresh_token = token['refresh_token']
access_token = token['token']
import oauth2
import imaplib
import email
emailid = 'k.abileva@gmail.com' 
oauth2String = oauth2.GenerateOAuth2String(client_id,access_token,base64_encode=False) #before passing into IMAPLib access token needs to be converted into string
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.authenticate('XOAUTH2', lambda x: oauth2String)
mail.select("inbox") # connect to inbox.
#rest of the code to play with emails
#ffor more info please check the link on top
