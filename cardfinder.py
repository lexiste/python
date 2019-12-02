#!/usr/bin/env python3

import re
import sys
import time

from termcolor import colored, cprint

def foundCard(line, cardType):
    # don't display the fill card number (line), so cut middle of string
    lineLen = len(line)
    pre = line[:4]
    post = line[(lineLen-4):]
    fillLen = lineLen - 8
    maskedLine = pre + '*' * fillLen + post
    #print colored('[!] Potential ' + cardType + ' card found. Regex Match: ' + maskedLine, 'red')
    print(colored('[!] ', 'red') + cardType + ' matched regex: ' + line)

def findCards(line):
    if re.match('^.*4\d{15}', line) is not None:
        cardType = 'Visa'
        foundCard(line, cardType)
    elif re.match('^.*5\d{15}', line) is not None:
        cardType = 'Mastercard'
        foundCard(line, cardType)
    elif re.match('^.*3[4,7]\d{13}', line) is not None:
        cardType = 'American Express'
        foundCard(line, cardType)

def usage():
    print(colored('[!!] pass file name as argument', 'red'))
    sys.exit(-1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    start = time.time()
    with open(sys.argv[1]) as fp:
        print('Looking for cards...\n')
        for line in fp:
            findCards(line.strip())
    end = time.time()
    print('\nCompleted execution in ' + str(end-start) + ' seconds')
