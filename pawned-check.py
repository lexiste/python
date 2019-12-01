
##
## pass in an account (email address) to search the haveibeenpwnd.com web
## site and return any/all breaches
## 

import requests
import json
import argparse

## accept a simple email addres
##  - next run simple regex for email check ?
parsed = argparse.ArgumentParser()
parsed.add_argument("account", help="email address to search for")
args = parsed.parse_args()

account = args.account
remoteURL = "https://haveibeenpwned.com/api/v2/breachedaccount/"

print("-" * 60)
print("Searching HaveIBeenPawned for", account)
print("-" * 60)

remoteURL += account
print("++} URL:", remoteURL)

web_request = requests.get(remoteURL)

print("++} status_code:", web_request.status_code)

## check the status code and if not successfull, then print the code and exit
if web_request.status_code != 200:
    print("Status:", web_request.status_code)
    exit(-1)

data = json.loads(web_request.text)

## nice formating dumped output of the json dictionary data blob
# print(json.dumps(data, indent=4))

## this works, however it outputs every key:value pair
##  we really only want to display Name, Domain, Description, BreachDate, DataClasses
## the for X in Y, X is not an interge, but a dictionary type meaning I need to
##  handle it differently, rough oupput with some formating
#for i in data:
#    for key, value in i.items():
#        print(key, ":", value)
for dict in data:
    print(dict['Name'], " ", dict['Domain'], " Breach Date:", dict['BreachDate'], "\n", dict['Description'],"\n")

