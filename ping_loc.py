#this function simulates a ping and returns 0 if machine could be pinged, not 0 otherwise

from platform   import system as system_name  # Returns the system/OS name
from subprocess import call   as system_call  # Execute a shell command
import subprocess

def ping(myhost):

    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """
    # Ping command count option as function of OS
    param = '-n 1' if system_name().lower()=='windows' else '-c 1'
    command = "ping %s %s" % (param,myhost)
    ping_response = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read() 
    #print("ping resp : %s" % ping_response)

    #will be something like this :
    #Pinging 192.168.0.147 with 32 bytes of data:
    #Reply from 192.168.0.147: bytes=32 time<1ms TTL=64
    #Ping statistics for 192.168.0.147:
    #    Packets: Sent = 1, Received = 1, Lost = 0 (0% loss),
    #Approximate round trip times in milli-seconds:
    #    Minimum = 0ms, Maximum = 0ms, Average = 0ms

    pingOK = True
    if ((b'unreachable' in ping_response.lower()) or (b'request timed out' in ping_response.lower())):
        pingOK = False

    return pingOK

#--------------------------------------

def testPing():
    #testing the function 

    myhost = "192.168.0.117"
    print("host %s : %s" % (myhost,ping(myhost)))

    myhost = "192.168.0.147"
    print("host %s : %s" % (myhost,ping(myhost)))

    myhost = "192.168.0.2"
    print("host %s : %s" % (myhost,ping(myhost)))

#main
testPing()