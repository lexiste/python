#!/usr/bin/python3

import requests
import json
import datetime
import optparse
import sys
import os
from requests.auth import HTTPBasicAuth

'''
  download a file from the PPS server using their published REST API's, saving the file
  locally then then read in that file and create a formatted output file with just a
  few of the columns we actually want to import, but keep the full file
'''

__version__ = "0.1.1"
__prog__ = "pp-quarantine"
__author__ = "todd fencl"
__contact__ = "todd.fencl@gmail.com"

EXIT_CODES = {
    "ok" 		: 0,
    "generic" 	: 1,
    "invalid" 	: 3,
    "missing" 	: 5,
    "limit" 	: 7
}

if __name__ == "__main__":
	'''
	  need to handle as part of the URI /rest/v1/quarantine?
		folder (required)
		from or rcpt (required)
		startdate (optional)
		output filename (required)
	'''

	conBaseURL = "https://00314801.pphosted.com:10000/"
	conAuthURL = conBaseURL + "/rest/v1/quarantine?folder=BitCoin%20Wallet&rcpt=*"

	# build the file name to write to using pps_YYYY-MM-DD_HHMM
	strStamp = datetime.datetime.now().strftime('%Y-%m-%d_%H%M')
	ppsFile = "pps_" + str(strStamp) + ".json"
	userFile = "pps_" + str(strStamp) + ".csv"

	try:
		response = requests.get(conAuthURL, auth=HTTPBasicAuth('apiaccount', '62cattleya!flaunche'))
		print('--------------------')
		print('API Call: {}'.format(conAuthURL))
		print('Status code: {}'.format(str(response.status_code)))
		print('Content-Type: {}'.format(response.headers['content-type']))
	except:
		print('Error ... : {}'.format(str(response.status_code)))
		exit('Could not load page, check connection')

	# open a file and write the resulting json response data

	fw = open(ppsFile, "w")
	fw.write(response.text)
	fw.close


#	print('response: {}'.format(response.text)')

    # load the response data from the web call into a json object for parsing
#    json_resp = json.loads(response.text)

'''
	fuser = open(userFile, "w")    # user file to write to
	finput = open(ppsFile, "r")    # generated file to read in
    fSize = os.path.getsize(ppsFile)
'''

#	if finput.mode == 'r':
'''
    if fSize > 0:
		line = finput.readlines()
		for i in line:
			fuser.write(i)
#			print(i)
	if jsonObject == []:
		print "No data was returned!"
	else:
		for rows in jsonObject:
			print 'subject' + rows['subject'] + ';'
			print 'date;' + str(rows['date'] + 'subject;' + rows['subject'] + 'folder;' + rows['folder'] + 'recipients;' + str(rows['rcpts']) + 'from;' + rows['from'])

    # close the file handlers since we are done using them
	fuser.close
	finput.close
'''
