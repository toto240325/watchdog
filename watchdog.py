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

requestTimeout = 1000 	# timeout for requests
delayBackup=datetime.timedelta(seconds=60*60*24 + 2*60*60)
delayGetLastWindow=datetime.timedelta(seconds=30*10000)
delayUploadingfile=datetime.timedelta(seconds=60*60*24*365)

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
        return "     "
    else:
        return "NOK->"


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



print ("python version : " + sys.version)
now1=datetime.datetime.now()
#time_str = time.strftime("%H:%M:%S", time.localtime())
#datetime_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#print(time_str)
print(now1.strftime('%Y-%m-%d %H:%M:%S'))



print("myHostname : "+myHostname)
print ("starting")

flog=open(myLogFile,"a")
flog.write("---------------------\n")
flog.write("Starting watchdog on %s\n" % (now1.strftime('%Y-%m-%d %H:%M:%S')))


#lastGetWindowStr = "2018-03-03 21:37:43";
#lastGetWindowDate = datetime.datetime.strptime(lastGetWindowStr, '%Y-%m-%d %H:%M:%S')

lastBackupDatetime = getLastEventDatetime("backup P702");
lastUploadingFileDatetime = getLastEventDatetime("uploading file");
lastGetWindowDatetime = getLastWindowDatetime();

isBackupOK =        (now1 <= lastBackupDatetime         + delayBackup)
isGetLastWindowOK = (now1 <= lastGetWindowDatetime      + delayGetLastWindow)
isUploadingFileOK = (now1 <= lastUploadingFileDatetime  + delayUploadingfile)


if (not isBackupOK) or (not isGetLastWindowOK) or (not isUploadingFileOK):
    print("at least one problem found; sending email !")

    msg =       myCheck(isBackupOK)           + "lastBackupDatetime       : " + lastBackupDatetime.strftime('%Y-%m-%d %H:%M:%S') + "\n"
    msg = msg + myCheck(isGetLastWindowOK)    + "lastGetWindowDatetime    : " + lastGetWindowDatetime.strftime('%Y-%m-%d %H:%M:%S') + "\n"
    msg = msg + myCheck(isUploadingFileOK)    + "lastUploadingFileDatetime: " + lastUploadingFileDatetime.strftime('%Y-%m-%d %H:%M:%S') + "\n"

    print(msg)
    '''
    print(myCheck(isBackupOK)           + "lastBackupDatetime       : " + lastBackupDatetime.strftime('%Y-%m-%d %H:%M:%S'))
    print(myCheck(isGetLastWindowOK)    + "lastGetWindowDatetime    : " + lastGetWindowDatetime.strftime('%Y-%m-%d %H:%M:%S'))
    print(myCheck(isUploadingFileOK)    + "lastUploadingFileDatetime: " + lastUploadingFileDatetime.strftime('%Y-%m-%d %H:%M:%S'))
    '''

    tmpfile=open(myTmpFile,"w")
    tmpfile.write(msg)
    tmpfile.close()
    sendEmail("my subject", "my body", myTmpFile)


now1=datetime.datetime.now()
flog.write("Ending watchdog on %s\n" % (now1.strftime('%Y-%m-%d %H:%M:%S')))
flog.close()

          






