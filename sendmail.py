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

def mySend(user_name, passwd, from_email, to_email, subject, body, htmlbody, myfileName):

    msg = MIMEMultipart()

    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject


        
    #-----------------------------------------------
  
    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(body, 'plain')
    part2 = MIMEText(htmlbody, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    #-----------------------------------------------

    #msg.attach( MIMEText(body) )

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


#import sendmail
#import datetime

def testMySend():
    now1=datetime.datetime.now()
    nowStr = now1.strftime('%Y-%m-%d %H:%M:%S')

    print("Starting on %s" % nowStr)

    user_name = "toto240325mailer@gmail.com"
    passwd = "Toto060502!n"
    from_email = "toto240325@gmail.com"
    to_email = "toto240325@gmail.com"
    subject = "this is my subject on " + nowStr
    body = "this is my email body"

    # Create the body of the message (a plain-text and an HTML version).
    htmlbody = """\
    <html>
    <head></head>
    <body>
    <FONT FACE="courier">
    """
    htmlbody = htmlbody + body + """\
        </FONT>
        <p>End of message<br>
        Here is a test <a href="http://www.python.org">link</a>.
        </p>
    </body>
    </html>
    """

    myfileName = "c:\\Users\\derruer\\mydata\\projects\\watchdog\\sendmailTest.py"

    #sendmail.mySend(user_name, passwd, from_email, to_email, subject, body, myfileName)
    mySend(user_name, passwd, from_email, to_email, subject, body, htmlbody, myfileName)
    print("email sent to %s" % (to_email))

#main
#testMySend()

