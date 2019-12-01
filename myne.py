#!/usr/bin/python

import time
import argparse
import logging
from termcolor import colored, cprint


def log(message, *values):
    if not values:
        print(message)
    else:
        values_str = ','.join(str(x) for x in values)
        print('[%s] %s:%s' % (datetime.now(), message, values_str))

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbosity", help="increase output information [1-3]", type=int)
parser.add_argument("-i", "--input", help="input file")
parser.add_argument("-o", "--output", help="output file")
parser.add_argument("-k", "--key", help="path to key file (private or public)")
parser.add_argument("-e", "--enc", help="encrypt the input file to output file")
parser.add_argument("-d", "--dec", help="decrypt the input file to output file")
parser.add_argument("-l", "--log", help="output log file, used if verbosity > 0")
args = parser.parse_args()

outvar = ("Starting: " + time.asctime(time.localtime(time.time())))
cprint(outvar, color="green")

if args.verbosity > 0:
    print("Setting log file to: %s" % args.log)
    logging.basicConfig(filename=args.log,level=logging.DEBUG)
    logging.basicConfig(format='%(asctime)s %(message)s')

if args.enc:
    print("will be encrypting file %s using key %s" % (args.input, args.key))
    if args.verbosity >= 1:
        logging.info("will encrypt $%s using key %s" % (args.input, args.key))
