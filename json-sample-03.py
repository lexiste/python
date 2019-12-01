import json

jsonString = '{"count":2,"records":[{"k1":"v1","k2":"v2","k3":"v3"}]}'
jsonObj = json.loads(jsonString)
print type(jsonString)
for key in jsonObj:
	value = jsonObj[key]
	print 'type value: ' + str(type(value))
	if isinstance(value, (list,)):
		print 'we have a list, handle it'
		print 'value is: ' + str(value)
		#for index in range(len(value)):
			#v2 = value(index)
			#print "index: " + str(index) + " value: " + v2
	print("k/v are ({}) = ({})".format(key, value))
	