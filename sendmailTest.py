'''Please Note in order to use this script, you need to enable your Gmail,
allow less secure applications use the Gmail services. You can also use other
APIs which are freely available
happy hacking!!!
'''

import sendmail
import datetime

now1=datetime.datetime.now()
nowStr = now1.strftime('%Y-%m-%d %H:%M:%S')

print("Starting on %s" % nowStr)

user_name = "toto240325mailer@gmail.com"
passwd = "Toto060502!n"
from_email = "toto240325@gmail.com"
to_email = "toto240325@gmail.com"
subject = "this is my subject on " + nowStr
body = "this is my email body"

myfileName = "c:\\Users\\derruer\\mydata\\projects\\watchdog\\sendmailTest.py"

sendmail.mySend(user_name, passwd, from_email, to_email, subject, body, myfileName)

