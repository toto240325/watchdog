'''Please Note in order to use this script, you need to enable your Gmail,
allow less secure applications use the Gmail services. You can also use other
APIs which are freely available
happy hacking!!!
'''

import datetime

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

def mySend(user_name, passwd, from_email, to_email, subject, body, myfileName):

    msg = MIMEMultipart()

    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach( MIMEText(body) )
    part = MIMEBase('application', "octet-stream")

    fo=open(myfileName,"rb")
    part.set_payload(fo.read() )
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="attachment_sendmailTest.py"')
    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(user_name, passwd)

    server.sendmail(from_email, to_email, msg.as_string())
    server.close()

#--------------------------------------------------------
