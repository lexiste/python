#!/usr/bin/env python3

import socket
from termcolor import colored, cprint

hostnames = ['westgate', 'renoftp', 'westsftp', 'nvrepsftp12-ext']
domains = ['innotrac.com', 'radial.com']

for h in hostnames:
   for d in domains:
      fqdn = str.join('.', (h,d))

      try:
         addr = socket.gethostbyname(fqdn)
         print('{} resolves to {}'.format(fqdn, addr))
      except socket.gaierror:
         print(colored('[!!] ', 'red') + 'could not resolve {}'.format(fqdn))
