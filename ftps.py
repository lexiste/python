#!/usr/bin/python3

# we need to run in python v3.x to have access to ssl_version

import ssl
from ftplib import FTP_TLS
import sys

if len(sys.argv) == 2:
    test_host = sys.argv[1]
    print('connecting and testing to: ' + test_host)
    ftps = FTP_TLS()

    # print commands and responses
    ftps.set_debuglevel(2)

    # connect to server, port, timeout
    ftps.connect(test_host, 21, 10)

    # SSLv[2|3] may not work if OpenSSL compiled with the approperiate OPENSSL_NO_SSL flag
    try:
        ftps.ssl_version = ssl.PROTOCOL_SSLv2
        print('[+] Successfull using SSLv2')
    except:
        print('[-] failed using SSLv2')
    try:
        ftps.ssl_version = ssl.PROTOCOL_SSLv3
        print('[+] Successfull using SSLv3')
    except:
        print('[-] failed using SSLv3')
    try:
        ftps.ssl_version = ssl.PROTOCOL_TLSv1
        print('[+] Successfull using TLSv1')
    except:
        print('[-] failed using TLSv1')
    try:
        ftps.ssl_version = ssl.PROTOCOL_TLSv1_1
        print('[+] Successfull using TLSv1_1')
    except:
        print('[-] failed using TLSv1_1')
    try:
        ftps.ssl_version = ssl.PROTOCOL_TLSv1_2
        print('[+] Successfull using TLSv1_2')
    except:
        print('[-] failed using TLSv1_2')

    print('completed testing...')
    ftps.close()

else:
    print('Usage: ' + str(sys.argv[0]) + ' hostname/IP')
    exit(0)
