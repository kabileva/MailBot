###################  Set UP #########################
from flask import Flask, render_template, request
from werkzeug import generate_password_hash, check_password_hash
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()

#MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'gmailbot'
app.config['MYSQL_DATABASE_DB'] = 'mailbot'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()
###################  End Set UP #########################



################## Functions ########################

# fetches unsent emails. Should be used together with update_email_stats()
def get_unsent_emails():
#	conn = mysql.connect()
#	cursor = conn.cursor()
    cursor.callproc('get_unsent_emails', args=())
    data = cursor.fetchall()
    conn.commit()
  #  cursor.close()
   # conn.close()
    return data   # then rows in data can be accessed as "for row in data: <do smth>"		

# after unsent emails have been fetched, it updates their statuses to "sent"
def update_email_stats():    
    cursor.callproc('update_email_stat', args=())
    data = cursor.fetchall()
    conn.commit()


# fetches unsent replies. Should be used together with update_reply_stats()
def get_unsent_replies():
	cursor.callproc('get_unsent_replies', args=())
	data = cursor.fetchall()
	conn.commit()
	return data   # then rows in data can be accessed as "for row in data: <do smth>" 

# after unsent replies have been fetched, it updates their statuses to "sent"
def update_reply_stats():
	cursor.callproc('update_reply_stat', args=())
	data = cursor.fetchall()
	conn.commit()


# get a list of users with FB ids and tokens from the tbl_users
# used as shown below
def get_users():
    cursor.callproc('get_users', args=())
    data = cursor.fetchall()
    conn.commit()
    return data
#users = get_users()
#for user in users:
#    print(user[0])         # user[0] - unique ID in the database. user[1] - FB_id. user[2] - token


# example: add_email((1,'olg@gmail.com','lunch',"Adil","what's up madafaka?",'2017-10-29 17:45:40', 0))
def add_email(email): # email - tuple of arguments	
	cursor.callproc('add_email', email)
	data = cursor.fetchall()
	conn.commit()	


def add_user(FB_id, token): # FB_id - int, token - JSON
    cursor.callproc('add_user', (FB_id, token, 0))
    data = cursor.fetchall()
    conn.commit()


def add_reply(reply): # reply - tuple of arguments. Works like add_email()
    cursor.callproc('add_reply', reply)
    data = cursor.fetchall()
    conn.commit()


# returns true if a user with a given FB_id exists
def user_exists(FB_id):
    args = [FB_id]
    cursor.callproc('user_exists', args)
    data = cursor.fetchone()
    if (data[0] == 0):
	return False
    else: 
	return True


def get_FB_id(user_id):
    args = [user_id]
    cursor.callproc('get_FB_id',args)
    data = cursor.fetchone()
    return data[1]


def get_email(email_id):
    
	args = [email_id]
	cursor.callproc('get_email', args)
	data = cursor.fetchone()
	#cursor.close()
	conn.commit()
	return data


# given user_id and sender_id, it fetches all old emails previously sent to the given user by the given recipient 
def get_old_emails(user_id, sender_id):
	args = [user_id, sender_id]
	cursor.callproc('get_old_emails', args)
	data = cursor.fetchall()
	var = []
	for email in data:
		var.append(email[5])
	result = '\n'.join(var)
	return result


#print(get_old_emails(88, 'olg'))
#add_user(8, '{"client_id": "931653727468-ncf4n4k90t8u0et2pj9808gn9h8rvkal.apps.googleusercontent.com","client_secret": "gKWtUvSK14mA6D9PmPDzXIlD","refresh_token": null,"scopes": "https://www.googleapis.com/auth/gmail.readonly","token": "ya29.GlsBBYeiZiDtnS5aomiDd7SnIGImEh_-SLJHow2RDRD8Ro3VEJLY_0aGPSszEZPOXB6JnFj6-wHJ_BJfmaule0LldrG5Gt0JPNP-DqTNjWp8cbRub3652tgtX9Ye","token_uri": "https://accounts.google.com/o/oauth2/token"}')    
   
 #_hashed_password = generate_password_hash(_password)
	
      
