#!/usr/bin/env python

#
# Pastebin Key Word Monitor
#
# Read in a file of keywords to search for, then scrape PastBin for all
#  pastes.  Once we have the ID's query and search for any of our keywords
#  if a match is found record the ID and send an email message with the
#  body of the pastebin record.
#

import os
import sys
import signal
import requests
import smtplib
import time
import json
import argparse

from email.mime.text import MIMEText

# some other variables we'll need
max_sleep_time = 120 # sleep timer for scraping pastebin, be nice to them
connection_timeout = 30 # if things go south or don't respond bail out at this point
blnDebugFlag = True # for debug output toggling, perhaps argument flag as well

def DebugOutput(strOut):
    print("[DBG] %s" % strOut)

def ErrorOutput(strOut):
    print("[ERR] %s" % strOut)

# quick read of any args passed, look for a -d / --debug passed and assign to bool flag var
p = argparse.ArgumentParser(description="Pastebin Keyword Monitor")
p.add_argument('-d', '--debug', action="store_true", default=False, dest='debug_val')
a = p.parse_args()

blnDebugFlag = a.debug_val # for debug output toggling, perhaps argument flag as well
if blnDebugFlag:
   DebugOutput("Enabled DEBUG mode, this is noisy")

'''
remove hardcoding the username / password information, mostly because this is kept in
github and well, passwords 
'''
try:
    with open("login.json", "r") as login_file:
        data = json.load(login_file)
        # now that we loaded password file, load the variables
        alert_email_account = data['gmail']['username']
        alert_email_password = data['gmail']['password']
        login_file.close()
except IOError as e:
    ErrorOutput("Could not access the login.json file to extract user information")
    ErrorOutput("Raised %s" % e)
    raise SystemExit(-1)

if blnDebugFlag:
    DebugOutput("[u] %s ... [p] %s" % (alert_email_account, alert_email_password))

try:
    with open("keywords.txt", "r") as fd:
        file_contents = fd.read()
        keywords = file_contents.splitlines()
        fd.close()
except IOError as e:
    ErrorOutput("Missing file .... keywords.txt is not found in local directory")
    ErrorOutput("Raised %s" % e)

if blnDebugFlag:
    DebugOutput("%s read from file" % str(keywords))

'''
using signals, this should allow a CTRL+C to break gracefully and not causing a
traceback crash in python
'''


def signal_handler(signal, frame):
    print("\nProgram exiting gracefully!")
    raise SystemExit(0)


signal.signal(signal.SIGINT, signal_handler)

'''
meat and potatoes of the script ... 
 1. pull in a list of recent posts from pastebin using the api_scraping API returning a JSON string
 2. parse the string and check against pastebin ID's that we have already processes, this 
    helps as we if we have a new post, we make a 2nd call to to get the actual post, verifing we only
    process 'new' posts
 3. loop through the list of keywords from the keywords.txt file checking to see if any of those
    words exist in the post, if we have a match add the relevant information for later use in notification 
'''


def check_pastebin(keywords):
    new_ids = []  # list ...
    paste_hits = {}  # dictionary ...

    # poll the pastebin API to collect a JSON string that we can parse next
    #  to extract the actual pastebin post
    # pastebin limits the max number of queries at a single time to 250
    try:
        r = requests.get("https://scrape.pastebin.com/api_scraping.php?limit=250")
        if blnDebugFlag:
            DebugOutput("request call to pastebin.com")
    except Exception as ex:
        ErrorOutput("%s" % ex)
        return paste_hits # send back an empty dictionary if error

    # make sure we have a valid response from pastebin.com before continuing
    if r.status_code != 200:
        ErrorOutput("Response code from pastebin.com (response code is %i) indicates an error in the call.  Exit function to escape crashing..." % r.status_code)
        return paste_hits  # send back the empty dictionary

    # randomly we receive, essentially, an empty response.  there is a header but the size is always 155, check the size and 
    #  break out if we detect
    if len(r.text) < 200:
        ErrorOutput("Response is to small (len %i), indicates no usable data in the response.  Exit function to escape crashing..." % len(r.text))
        if blnDebugFlag:
            DebugOutput("%s" % r.text)
        return paste_hits  # send back the empty dictionary

    # this is more for "what just happened" we write the api_scraping JSON reply to a log file, just overwriting it every run
    # make sure to encode the data to handle UTF-8 which will include foreign characters
    with open("pastebin_response", "w") as fd:
        fd.write(r.text)
        fd.close()

    # response contains a JSON dataset and documentation can be found https://pastebin.com/api_scraping_faq
    result = r.json()

    # create or load a list of stored ID's that we have previously processed so we don't duplicate our work cycles
    if os.path.exists("pastebin_ids.txt"):
        with open("pastebin_ids.txt", "rb") as fd:
            pastebin_ids = fd.read().splitlines()
            fd.close()

    else:
        pastebin_ids = []

    for post in result:

        if post['key'] not in pastebin_ids:
            new_ids.append(post['key'])

            '''
            we have a new paste ID, so send a secondary request for the post
            this will be the actual post (paste??) with data
            see the requests web documents @ https://docs.python-requests.org/en/master/

            let's see if adding small timer and a try/except handler we can stop crashing
            during execution with 'Connection aborted' or 'ConnectionResetError(Connection reset by peer)' errors
            '''
            request_get_start = time.time()
            try:
                if blnDebugFlag:
                    DebugOutput("scrape_url: %s %s" % (post['scrape_url'], time.strftime("%d-%b-%y %H:%M:%S")))
                paste_response = requests.get(post['scrape_url'])
            # handling requests exceptions 
            #  [http://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions]
            except requests.exceptions.Timeout:
               ErrorOutput("reached TimeOut in request")
               if time.time() > request_get_start + connection_timeout:
                    raise Exception("Unable to perform requests.get() after {} seconds of ConnectionErrors.".format(connection_timeout))
               else:
                    time.sleep(2)
            except requests.exceptions.RequestException as caught_err:
                ErrorOutput("caught an error: %s" % caught_err)
                ErrorOutput("error arguments: %s" % caught_err.args)
                raise SystemExit(-1)

            # convert the text to lower case for searching
            paste_body_lower = paste_response.text.lower()

            keyword_hits = []

            for word in keywords:

                if word.lower() in paste_body_lower:
                    keyword_hits.append(word)

                    if blnDebugFlag:
                        DebugOutput("found keyword in paste %s appending to list" % word)

            if len(keyword_hits):
                paste_hits[post['key']] = (keyword_hits, paste_response.content)
                if blnDebugFlag:
                    DebugOutput("keywords %s" % str(keyword_hits))

                print("[*] Scored hit for %s %s" % (str(keyword_hits), post['full_url']))

                # write a line out to a greatest hits file with the date, key word(s) and URL for tracking along with email
                with open("pastebin_hits.txt", "a") as fd:
                    fd.write("%s; %s; %s \r\n" % (time.strftime("%d-%b-%y %H:%M:%S"), str(keyword_hits), post['full_url']))
                fd.close()

            # duplicate emails were being sent, try moving the write to inside the `if post['key']` block
            #
            # store these newly checked ID's in the hits file so we don't process again
            with open("pastebin_ids.txt", "a") as fd:
                for pastebin_id in new_ids:

                    if bidlnDebugFlag:
                        DebugOutput("pastebin_id in list (%s) written to %s file" % (pastebin_id, fd.name))

                    fd.write("%s\r\n" % pastebin_id)
            fd.close()

    print("[+] Successfully processed %d pastebin posts at %s" % (len(new_ids), time.strftime("%d-%b-%Y %H:%M:%S")))

    return paste_hits


'''
function that will takes our results and send us an email alert 

result passed in is a dictionary object that we can loop through and generate 
an email message using GMail
'''


def send_email_alert(result):
    email_body = "We found a matched keyword in our pastebin monitor!\r\n\r\n"

    if blnDebugFlag:
        DebugOutput("result passed to send_email_alert:\r\n %s" % str(result))
        #DebugOutput("[smtp-len] appear to be %i keys" % len(result.keys()))

    for paste_id in result:
        if blnDebugFlag:
            DebugOutput("[smtp-key] sending email for id %s" % paste_id)
            #DebugOutput("[smtp-msg] " + result[paste_id][1].decode('utf-8'))

        email_body = "We found a matched keyword in our pastebin monitor!\r\n\r\n"
        email_body += "\r\nPastebin Link: https://pastebin.com/" + paste_id
        email_body += "\r\nPastebin Keyword(s): " + ".".join(result[paste_id][0])
        email_body += "\r\nPastebin Body: " + result[paste_id][1].decode('utf-8')

        msg = MIMEText(email_body)
        msg['Subject'] = "Pastebin OSINT Keyword Match (%s)" % paste_id
        msg['From'] = alert_email_account
        msg['To'] = alert_email_account

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(alert_email_account, alert_email_password)

        try:
            server.sendmail(alert_email_account, alert_email_account, msg.as_string())
        except Exception as ex:
            ErrorOutput("Error delivering message to gmail.com (%s)" % ex)

        server.quit()

        print("[!] Alert email has been sent at %s " % time.strftime("%d-%b-%y %H:%M:%S"))

    return


'''
lack of better term ... main
'''

while True:

    time_start = time.time()

    result = check_pastebin(keywords)

    if blnDebugFlag:
        DebugOutput("check_pastebin returned %s" % str(result))

    # time to see if we have a hit, and send an email off as needed
    if len(result):
        if blnDebugFlag:
            DebugOutput("calling send_email_alert")

        send_email_alert(result)

    time_end = time.time()

    exec_time = time_end - time_start

    if exec_time < max_sleep_time:
        sleep_time = max_sleep_time - exec_time
        #print("[+] Sleeping for %i seconds" % sleep_time)
        time.sleep(sleep_time)
