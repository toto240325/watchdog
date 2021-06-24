#this function simulates a ping and returns 0 if machine could be pinged, not 0 otherwise

from platform   import system as system_name  # Returns the system/OS name
from subprocess import call   as system_call  # Execute a shell command
import subprocess
import sys


def ping(myhost):

    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """
    # Ping command count option as function of OS
    param = '-n 1 -w 2' if system_name().lower()=='windows' else '-c 1 -w 2'
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

    #print("ping response :>"+ping_response+"<")
    if ping_response == "":
      return False
    pingOK = True
    if ((b'100% loss' in ping_response.lower()) or 
        (b'100% packet loss' in ping_response.lower()) or 
        (b'unreachable' in ping_response.lower()) or 
        (b'request timed out' in ping_response.lower())
        ):
        pingOK = False

    return pingOK

#--------------------------------------

def testPing():
    #testing the function 

    myhost = "192.168.0.98"
    print("host %s : %s" % (myhost,ping(myhost)))

    myhost = "192.168.0.147"
    print("host %s : %s" % (myhost,ping(myhost)))

    myhost = "192.168.0.99"
    print("host %s : %s" % (myhost,ping(myhost)))

def main():
  testPing()
  l = len(sys.argv)
  print 'Number of arguments:', l, 'arguments.'
  print 'Argument List:', str(sys.argv)
  print("script name : " + sys.argv[0])
  if l > 1:
    print("first arg : " + sys.argv[1])
    myhost = sys.argv[1]
    print("host %s : %s" % (myhost,ping(myhost)))
 
if __name__ == "__main__":
   
  main()
