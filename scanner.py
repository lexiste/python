import socket
import os
import sys

def retBanner(ip, port):
    try:
        socket.setdefaulttimeout(2)
        s = socket.socket()
        s.connect((ip, port))
        banner = s.recv(1024)
        return banner
    except:
        return

def checkVulns(banner, filename):
    f = open(filename, 'r')
    for line in f.readlines():
        if line.strip('\n') in banner:
            print '[!!] Server is vulnerable: ' + banner.strip('\n')

def main():
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        if not os.path.isfile(filename):
            print '[-] ' + filename + ' does not exist.'
            exit(0)
            if not os.access(filename, os.R_OK):
                print '[-] ' + filename + ' access denied.'
                exit(0)
    else:
        print '[-] Usage: ' + str(sys.argv[0]) + ' <vuln filename>'
        exit(0)

    portList = [21,22,80,443,5900]
    for x in range(150, 170): # range of hosts to scan for, not ideal
        ip = '10.0.0.' + str(x)
        for port in portList:
            banner = retBanner(ip, port)
            if banner:
                print '[+] ' + ip + ':' + str(port) + ' -- ' + banner, # keep the trailing comma, new line supression trick
                checkVulns(banner, filename)

if __name__ == '__main__':
    main()
