#!/usr/bin/python3.7

import json
from huepy import *
import argparse
import os
import requests
import sys
from termcolor import colored
from terminaltables import SingleTable
import subprocess
from pathlib import Path

def check_response_code(resp):
    if resp.status_code == 204:
        print(bad("Request rate limit exceeded"))
        sys.exit()

def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("FILE", help="File containing hashes, binary, hash string or directory")
    parser.add_argument("-k", "--key", dest='KEY', metavar="<api_key>", action="store", default=api_key, help="Specify VT API key")
    parser.add_argument("-q", "--quiet", dest="QUIET", action="store_true", help="Do not print vendor analysis results")
    parser.add_argument("-p", "--positive", dest="POSITIVE", action="store_true", help="Show only positive results in vendor analysis")
    parser.add_argument("-o", "--out", dest="OUT", action="store_true", help="Save JSON response to a file")
    parser.add_argument("-c", "--clear", dest="CLEAR", action="store_true", help="Clear screen before printing vendor analysis results ")
    res = parser.parse_args()
    return res

def main():
    res = arguments()
    api_key = res.KEY
    file_to_scan = res.FILE
    params = {"apikey":api_key}
    files = {"file":(res.FILE, open(res.FILE, 'rb'))}
    resp = requests.post('https://www.virustotal.com/vtapi/v2/file/scan', files=files, params=params)
    check_response_code(resp)
    print("[*] Sent file to VT api")
    resource_hash = resp.json()['resource']
    params['resource'] = resource_hash
    headers = {
        "Accept-Encoding": "gzip, deflate",
        "User-Agent":      "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0"
    }
    resp = requests.get("https://www.virustotal.com/vtapi/v2/file/report", params=params, headers=headers)
    check_response_code(resp)
    if res.OUT:
        with open(res.OUT, "w+") as outfile:
            outfile.write(resp.text)
            outfile.close()
    print("[*] Received response\n")
    positives = int(resp.json()['positives'])
    total = int(resp.json()['total'])
    if res.CLEAR:
        subprocess.call("clear", shell=True)
    detection_rate = round((positives/total)*100, 2)
    attrs = []
    if int(detection_rate) in range(0, 20):
        color = 'blue'
    elif int(detection_rate) in range (20, 40):
        color = 'green'
    elif int(detection_rate) in range (40, 60):
        color = 'yellow'
    elif int(detection_rate) in range (60, 80):
        color = 'red'
    elif int(detection_rate) in range (60, 100):
        color = 'red'
        attrs = ['blink']
    print(f"{green('[+]')} Results for {bold(res.FILE)} ({resp.json()['scan_date']})")
    print(f"Permalink: {resp.json()['permalink']}")
    print(f"\n{bold('Detection rate:')} {colored(detection_rate, color, attrs=attrs)} ({green(positives)} positive / {red(total-positives)} negative)")
    print(f"MD5: {resp.json()['md5']}")
    print(f"SHA256: {resp.json()['sha256']}")
    print(f"SHA1: {resp.json()['sha1']}")
    scans = resp.json()['scans']
    table_data = [['--VENDOR--', '--STATUS--', '--RESULT--', '--UPDATE--']]
    for scan in scans:
        detected = colored("not detected", "red", attrs=["bold"])
        scan_result = "N/A"
        if scans[scan]['detected']:
            detected = colored("detected", "green", attrs=["bold"])
        if scans[scan]['result'] != None:
            scan_result = scans[scan]["result"]
        date = str(scans[scan]['update'])
        date = "{}-{}-{}".format(date[0:4], date[4:6], date[6:8])
        if (res.POSITIVE and scans[scan]["detected"]):
            table_data.append([scan, detected, scan_result, date])
        elif not res.POSITIVE:
            table_data.append([scan, detected, scan_result, date])
    table = SingleTable(table_data)
    table.inner_column_border = False
    table.outer_border = False
    table.justify_columns[1] = "center"
    if (not res.QUIET and len(table_data) != 1):
        print("\nVendors analysis results:\n")
        print(table.table)

if __name__ == "__main__":
    data_path = Path("~/scripts/")
    data_file = data_path / "login.json"
    #print("data path name: %s\ndata file name: %s\ndata file expand: %s" % (data_file.parent, data_file.name, data_file.expanduser()))
    if not data_file.expanduser().is_file():
        print(f"{red('[!]')} Could not locate the login.json file in path %s" % data_file.expanduser())
        raise SystemExit(-1)
    else:
        fp = data_file.expanduser()
        with open(fp, "r") as fh:
            data = json.load(fh)
            api_key = data['virustotal']['apikey']
            #print("Recovered VT API KEY: %s" % api_key)
            fh.close()
            fp = ""

    try:
        print("%s" % fp)
        main()
    except KeyboardInterrupt:
        print("\n[*] Exiting...")
