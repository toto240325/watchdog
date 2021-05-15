#  !/usr/bin/env python
#
import mysendmail
import datetime
import params
import socket
import sys

thisScript = sys.argv[0]

now1=datetime.datetime.now()
nowStr = now1.strftime('%Y-%m-%d %H:%M:%S')

hostname = socket.gethostname()
mailer = params.mailer
mailer_pw = params.mailer_pw
from_email = params.from_email
to_email = params.to_email
subject = "Test from " + thisScript + " on " + hostname + " at " + nowStr
body = "body"
htmlbody = "htmlbody"
   
myTmpFile = "/tmp/watchdog.tmp"
tmpfile=open(myTmpFile,"w")
tmpfile.write("msg")
tmpfile.close()

print ("test10")
print ("sendmail %s, %s, %s, %s, %s, %s, %s" % (mailer, mailer_pw, from_email, to_email, subject, body, htmlbody))
mysendmail.mySend(mailer, mailer_pw, from_email, to_email, subject, body, htmlbody, myTmpFile)
print ("test11")

          






