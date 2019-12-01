
import socket

def retBanner(ip, port):
    try:
        socket.setdefaulttimeout(2)
        s = socket.socket()
        s.connect((ip, port))
        banner = s.recv(1024)
        return banner
    except:
        return

def checkVuln(banner):
    if 'FreeFloat Ftp Server' in banner:
        print '[+] FreeFloat FTP server vuln'
    elif '3Com 3CDaemon FTP Server Version 2.0' in banner:
        print '[+] 3Com FTP server vuln'
    elif 'Ability Server 2.34' in banner:
        print '[+] Ability FTP server vuln'
    elif 'Samo FTP Server 2.0.2' in banner:
        print '[+] Sami FTP server vuln'
    else:
        print '[-] FTP server not found vuln'
    return

def main():
    ip1 = '8.8.8.8'
    ip2 = '192.168.81.130'
    ip3 = '10.0.0.199'
    port = 21

    b1 = retBanner(ip1, port)
    if b1:
        print '[+] ' + ip1 + ': ' + b1.strip('\n')
        checkVuln(b1)
    b2 = retBanner(ip2, port)
    if b2:
        print '[+] ' + ip2 + ': ' + b2.strip('\n')
        checkVuln(b2)

if __name__ == '__main__':
    main()
