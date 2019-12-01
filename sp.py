
import socket
import subprocess
import sys
from datetime import datetime
import argparse

## allow the user to pass input through the command line, or prompt them ...
parser = argparse.ArgumentParser()
parser.add_argument("host")
parser.add_argument("port")
args = parser.parse_args()
#print("host: ", args.host, ":", args.port)

remoteServerIP = socket.gethostbyname(args.host)
remotePort = args.port

#
#remoteServer = input("Enter remote host to scan: ")
#remoteServerIP = socket.gethostbyname(remoteServer)
#remotePort = input("Enter report port to check: ")

## provide some header information
print("-" * 60)
print("Scanning remote host ", remoteServerIP,":",remotePort)
print("-" * 60)

## for later, how long we ran
t1 = datetime.now()

try:
   sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   ## use connect_ex to raise an error indicator instead of raising an exception
   result = sock.connect_ex((remoteServerIP, int(remotePort)))
   if result == 0:
      ## create a string to send so the remote side responds with ?something?
      ## if we don't do this, we just have an open connection whic is sort of meh
      byte = str.encode("Server:\r\n")
      print(byte)
      sock.send(byte)
      ## grab the first 512 bytes returned, could be more but we don't need much,
      ## later recon would be done for sigint
      banner = sock.recv(512)
      print("Port {}:  Open ".format(remotePort))
      print(banner)
   sock.close()

except KeyboardInterrupt:
   sys.exit()

except socket.gaierror:
   print("Hostname could not be resolved.  Exiting")
   sys.exit()

except socket.error:
   print("Couldn't connect to server")
   print("-" * 60)
   sys.exit()

t2 = datetime.now()

total = t2 - t1

print("Scan Completed in: ", total)
print("-" * 60)
