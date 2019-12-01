import requests
import json

try:
	response = requests.get('http://jsonplaceholder.typicode.com/users')
except:
	exit('could not load page, check connection')
	
#print response.text
print "response.text type: " + str(type(response.text))
print(json.loads(response.text))
jsonUsers = json.loads(response.text)

print " "
print "Status code: " + str(response.status_code)
print "Content-Type: " + response.headers['content-type']

data = response.json()
print "Number of objects returned: " + str(len(data))
print "--FOR EACH--"
if jsonUsers == []:
	print 'no data returned'
else:
	for rows in jsonUsers:
		print 'rec id:' + str(rows['id']) + ' username: ' + rows['username'] + ' website: ' + rows['website']