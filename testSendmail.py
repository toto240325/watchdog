#  !/usr/bin/env python
#

import sendmail
import datetime
import params

now1=datetime.datetime.now()
nowStr = now1.strftime('%Y-%m-%d %H:%M:%S')

mailer = params.mailer
mailer_pw = params.mailer_pw
from_email = params.from_email
to_email = params.to_email
subject = "Test from testSendmail on " + nowStr
body = "body"
htmlbody = "htmlbody"
   
myTmpFile = "/home/toto/projects/watchdog/watchdog.tmp"
tmpfile=open(myTmpFile,"w")
tmpfile.write("msg")
tmpfile.close()

print ("test10")
print ("sendmail %s, %s, %s, %s, %s, %s, %s" % (mailer, mailer_pw, from_email, to_email, subject, body, htmlbody))
sendmail.mySend(mailer, mailer_pw, from_email, to_email, subject, body, htmlbody, myTmpFile)
print ("test11")

          






