from database.database import get_email
from mbot import Mbot

mbot = Mbot()

print(mbot.get_old_emails(87, 'olg@gmail.com'))     
