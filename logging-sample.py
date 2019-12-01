#!/usr/bin/python3

import time
import argparse

##https://docs.python.org/3/howto/logging.html#a-simple-example
import logging

def log(message, *values):
	if not values:
		print(message)
	else:
		values_str = ', '.join(str(x) for x in values)
		print('[%s] %s: %s' % (datetime.now(), message, values_str))


parser = argparse.ArgumentParser()
parser.add_argument("string", help="echo the string you use here")
parser.add_argument("-v", "--verbosity", help="increase output information", type=int)
parser.add_argument("-iF", "--inputFile", help="input list of hosts/networks to check")
parser.add_argument("-oF", "--outputFile", help="output file")
parser.add_argument("-iD", "--inputDict", help="keyword list for checking")
args = parser.parse_args()
if args.verbosity == 2:
   print("verbosity level 2")
elif args.verbosity == 1:
   print("verbosity level 1")
else:
   print("verbosity off")

print("Starting: " + time.asctime(time.localtime(time.time())))
if args.inputFile:
	print("iF: " + args.inputFile)

if args.outputFile:
	print("oF: " + args.outputFile)
        logging.basicConfig(filename=args.outputFile,level=logging.DEBUG)
        logging.basicConfig(format='%(asctime)s %(message)s')

if args.inputDict:
	print("iD: " + args.inputDict)
print("Starting: " + time.asctime(time.localtime(time.time())))

if args.outputFile:
   logging.info(args.string)
else:
   log(args.string)

time.sleep(15)
log(args.string)

print("Starting: " + time.asctime(time.localtime(time.time())))
