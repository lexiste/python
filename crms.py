#!/usr/bin/python3

import socket

hostnames = ['westgate', 'renoftp', 'westsftp', 'nvrepsftp12-ext']
domains = ['innotrac.com', 'radial.com']

for h in hostnames:
   for d in domains:
      fqdn = str.join('.', (h,d))

      try:
         addr = socket.gethostbyname(fqdn)
         print('{} {}'.format(fqdn, addr))
      except socket.gaierror:
         print('[!!] server not resolved {}'.format(fqdn))
