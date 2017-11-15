from flask import Flask, render_template, request
from werkzeug import generate_password_hash, check_password_hash
from flask.ext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()

#MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'gmailbot'
app.config['MYSQL_DATABASE_DB'] = 'mailbot'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route("/")
def main():
    conn1 = mysql.connect()
    cursor1 = conn1.cursor()
    conn2 = mysql.connect()
    cursor2 = conn2.cursor()
    
    #_hashed_password = generate_password_hash(_password)
    value = None
  #  cursor1.callproc('add_user', (3, '{"name": "Kate"}', 0))   
   # cursor1.callproc(" INSERT INTO tbl_users (user_FB_id, user_token) Values(5, {'Alish': 'loh'})")
    cursor1.callproc('add_user', (7, '{"client_id": "931653727468-ncf4n4k90t8u0et2pj9808gn9h8rvkal.apps.googleusercontent.com","client_secret": "gKWtUvSK14mA6D9PmPDzXIlD","refresh_token": null,"scopes": "https://www.googleapis.com/auth/gmail.readonly","token": "ya29.GlsBBYeiZiDtnS5aomiDd7SnIGImEh_-SLJHow2RDRD8Ro3VEJLY_0aGPSszEZPOXB6JnFj6-wHJ_BJfmaule0LldrG5Gt0JPNP-DqTNjWp8cbRub3652tgtX9Ye","token_uri": "https://accounts.google.com/o/oauth2/token"}', 0))
    #cursor1.callproc(" INSERT INTO tbl_users (user_FB_id, user_token) Values (5, '{'client_id': '931653727468-ncf4n4k90t8u0et2pj9808gn9h8rvkal.apps.googleusercontent.com','client_secret': 'gKWtUvSK14mA6D9PmPDzXIlD','refresh_token': null,'scopes': 'https://www.googleapis.com/auth/gmail.readonly','token': 'ya29.GlsBBYeiZiDtnS5aomiDd7SnIGImEh_-SLJHow2RDRD8Ro3VEJLY_0aGPSszEZPOXB6JnFj6-wHJ_BJfmaule0LldrG5Gt0JPNP-DqTNjWp8cbRub3652tgtX9Ye','token_uri': 'https://accounts.google.com/o/oauth2/token'}') ")  
    

    #cursor2.callproc('add_email',(1,1,'meeting',"Kate","what's up madafaka?",'2017-10-29 17:45:40'))
    #conn2.commit() # should be commited after add_user due to foreign key constrains
    data = cursor1.fetchall()
    if len(data) is 0:
       conn1.commit()
     #  conn2.commit()
       return "data has been successfully added!"
    else:
       conn2.commit()
       return "data hasn't been added"
    

if __name__ == "__main__":
    app.run()

