from gbot import Gbot
gbot = Gbot()
import time
import socket

n = 0
for i in range(100):
   
    subj = 'Subject:'+str(time.time())
    print(subj)
    try:
        gbot.send_email(835227646602037, 'altortay@gmail.com', subj, 'testtest')
    except socket.error:
        continue
    n = n + 1
print(n)

