#  !/usr/bin/env python
# this script checks a few things around and sends an email if something is weird
#

import os
import sys
import socket
import time
import datetime
import subprocess
import json
import requests
from platform   import system as system_name  # Returns the system/OS name
from subprocess import call   as system_call  # Execute a shell command

import sendmail
from ping import ping


requestTimeout = 1000 	# timeout for requests
delayBackup=datetime.timedelta(seconds=60*60*24 + 2*60*60)
delayUploadingfile=datetime.timedelta(seconds=60*60*24*365)
#delay to check for GetLastWindow depend on whether mypc3 is up or down
shortDelayGetLastWindow=datetime.timedelta(seconds=30)
longDelayGetLastWindow=datetime.timedelta(seconds=60*60*24*10) # 10 days

systematicEmailSendTime = 20  # always send an email at that time of the day, even if everything OK


mypc3 = "192.168.0.2"

myHostname = socket.gethostname()

if myHostname == "L02DI1453375DIT":
    myTmpFile = "C:\\Users\\derruer\\mydata\\mytemp\\watchdog.tmp"
    myLogFile = "C:\\Users\\derruer\\mydata\\mytemp\\watchdog.log"
else:
    myTmpFile = "/home/toto/projects/watchdog/watchdog.tmp"
    myLogFile = "/home/toto/projects/watchdog/watchdog.log"




def getLastEventDatetime(eventType):
    url = 'http://192.168.0.147/monitor/getEvent.php?eventFct=getLastEventByType&type='+eventType
    r = requests.get(url, timeout=requestTimeout)
    #print(r.content)
    # r.content supposed to be something like this : 
    #   {"records":[{"id":"254","time":"2018-03-03 21:37:43","host":"L02DI1453375DIT","text":"incremental backup P702 to googleDrive via mypc3","type":"backup P702"}],"errMsg":""}\
    j=json.loads(r.content)
    lastEventDatetimeStr= j['records'][0]['time']
    #print("URL : " + url + "   eventType : " + eventType + "   finished on " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    myDatetime = datetime.datetime.strptime(lastEventDatetimeStr, '%Y-%m-%d %H:%M:%S')
    return myDatetime

def getLastWindowDatetime():
    url = 'http://192.168.0.147/monitor/getLastTimeWindowTitle.php'
    r = requests.get(url, timeout=requestTimeout)
    #print(r.content)
    j=json.loads(r.content)
    lastEventDatetimeStr= j['time']
    myDatetime = datetime.datetime.strptime(lastEventDatetimeStr, '%Y-%m-%d %H:%M:%S')
    return myDatetime


def myCheck(myBool):
    if myBool: 
        return '<p style="color:black;">'
    else:
        return '<p style="color:red;">NOK->'


def sendEmail(subject,body,attachedFileStr):
    cmd = ('sendEmail -f toto240325@gmail.com -t toto240325@gmail.com -u "%s" -m "%s" -s smtp.voo.be:25 -a %s' % (subject,body,attachedFileStr))
        
    if myHostname == "L02DI1453375DIT":
        print ("!!!!!!!!!!!!! just sent an email !!!!!!!!!!")
        flog.write("!!!!!!!!!!!!! just sent an email !!!!!!!!!!\n")
        print (cmd)
    else:
        flog.write("executing : " + cmd+'\n')
        print (cmd)
        ostemp = os.popen(cmd).readline()
        print("ostemp : " + ostemp)
        flog.write("result : " + ostemp + '\n')


#print ("python version : " + sys.version)
now1=datetime.datetime.now()
#time_str = time.strftime("%H:%M:%S", time.localtime())
#datetime_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
nowStr = now1.strftime('%Y-%m-%d %H:%M:%S')
print("Starting on " + nowStr)
print("myHostname : "+myHostname)

flog=open(myLogFile,"a")
flog.write("---------------------\n")
flog.write("Starting watchdog on %s\n" % (now1.strftime('%Y-%m-%d %H:%M:%S')))


#lastGetWindowStr = "2018-03-03 21:37:43";
#lastGetWindowDate = datetime.datetime.strptime(lastGetWindowStr, '%Y-%m-%d %H:%M:%S')

lastBackupDatetime = getLastEventDatetime("backup P702");
lastUploadingFileDatetime = getLastEventDatetime("uploading file");
lastGetWindowDatetime = getLastWindowDatetime();

isBackupOK =        (now1 <= lastBackupDatetime         + delayBackup)

# if mypc3 is up then check if getwindow was OK very recently, otherwise check that it ran at least 24h ago
mypc3Up = ping(mypc3)
if (mypc3Up):
    isGetLastWindowOK = (now1 <= lastGetWindowDatetime      + shortDelayGetLastWindow)
else:
    isGetLastWindowOK = (now1 <= lastGetWindowDatetime      + longDelayGetLastWindow)


isUploadingFileOK = (now1 <= lastUploadingFileDatetime  + delayUploadingfile)

msg ="everything seems to be OK"

sendAnyway = (now1.hour <= systematicEmailSendTime) and (now1.hour+1 > systematicEmailSendTime)

if ((not isBackupOK) or 
    (not isGetLastWindowOK) or 
    (not isUploadingFileOK) or
    sendAnyway
    ):
    
    if not sendAnyway: 
        print("at least one problem found; sending email !")
    if sendAnyway:
        print("sending anywy because it's time to recap the situation")
    

    msg = "(NB : mypc3 is %s)" % ("up" if mypc3Up else "down") + "\n<p>"
    msg = msg + myCheck(isBackupOK)           + "lastBackupDatetime       : " + lastBackupDatetime.strftime('%Y-%m-%d %H:%M:%S') + "\n<p>"
    msg = msg + myCheck(isGetLastWindowOK)    + "lastGetWindowDatetime    : " + lastGetWindowDatetime.strftime('%Y-%m-%d %H:%M:%S') + "\n<p>"
    msg = msg + myCheck(isUploadingFileOK)    + "lastUploadingFileDatetime: " + lastUploadingFileDatetime.strftime('%Y-%m-%d %H:%M:%S') + "\n<p>"

    '''
    print(myCheck(isBackupOK)           + "lastBackupDatetime       : " + lastBackupDatetime.strftime('%Y-%m-%d %H:%M:%S'))
    print(myCheck(isGetLastWindowOK)    + "lastGetWindowDatetime    : " + lastGetWindowDatetime.strftime('%Y-%m-%d %H:%M:%S'))
    print(myCheck(isUploadingFileOK)    + "lastUploadingFileDatetime: " + lastUploadingFileDatetime.strftime('%Y-%m-%d %H:%M:%S'))
    '''

    tmpfile=open(myTmpFile,"w")
    tmpfile.write(msg)
    tmpfile.close()


    user_name = "toto240325mailer@gmail.com"
    passwd = "Toto060502!n"
    from_email = "toto240325@gmail.com"
    to_email = "toto240325@gmail.com"
    subject = "Watchdog on " + nowStr
    body = msg

    htmlbody = """\
    <html>
    <head></head>
    <body>
    <FONT FACE="courier">
    """
    htmlbody = htmlbody + body + """\
        </FONT>
    </body>
    </html>
    """
    

    sendmail.mySend(user_name, passwd, from_email, to_email, subject, body, htmlbody, myTmpFile)

print(msg)
flog.write(msg)
    
now1=datetime.datetime.now()
flog.write("Ending watchdog on %s\n" % (now1.strftime('%Y-%m-%d %H:%M:%S')))
flog.close()

          






