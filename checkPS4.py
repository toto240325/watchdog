#  !/usr/bin/env python
#

import mysendmail
import datetime
import params
import socket
import sys
from ping import ping
from time import sleep

def mySimpleSendMail(subject,body,to):
  mailer = params.mailer
  mailer_pw = params.mailer_pw
  from_email = params.from_email
  htmlbody = "htmlbody"
  myTmpFile = "/tmp/watchdog.tmp"
  tmpfile=open(myTmpFile,"w")
  tmpfile.write("msg")
  tmpfile.close()
  mysendmail.mySend(mailer, mailer_pw, from_email, to, subject, body, htmlbody, myTmpFile)

def mailNotif(to_email,thisScript):
  now1=datetime.datetime.now()
  nowStr = now1.strftime('%Y-%m-%d %H:%M:%S')
  hostname = socket.gethostname()
  subject = "PS4 up (test from " + thisScript + " on " + hostname + " at " + nowStr + ")"
  body = "this is the body"
  print("PS4 up")
  print ("mySimpleMail(%s, %s, %s)" % (subject, body, to_email))
  mySimpleSendMail(subject,body,to_email)

def log(bStatus):
  now1=datetime.datetime.now()
  nowStr = now1.strftime('%Y-%m-%d %H:%M:%S')
  mylog = "/tmp/PS4.log"
  msg = nowStr + " PS4 is " + ("Up" if bStatus else "Down")
  print msg
  f = open(mylog,"a")
  f.write(msg + "\n")
  f.close()

# main ---------------------------------------------------

thisScript = sys.argv[0]

to_email = params.to_email
PS4 = "192.168.0.40"

sec = 0
while True:
  try:
    if sec % 60 == 0:
      log(ping(PS4))

    if sec % 60*10 == 0:
      if ping(PS4):
        mailNotif(to_email,thisScript)

  except Exception as error:
    msg = "there was an exception : " + str(error)
    print(msg)
    mySimpleSendMail("Problem with script " + thisScript + " (exception !)",msg,to_email)
    triggerCompressor(0)
    turnRedLed(0)

  sec += 1
  sleep(1)



