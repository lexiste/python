#!/usr/bin/env python3

import base64
text1 = 'this is a string'.encode()
text2 = 'https://fencl.net'.encode()

# prep the string into byte-like object
#encodeBytes = base64.urlsafe_b64encode(text1.encode("utf-8"))
#encodeStr = str(encodeBytes, "utf-8")

print(text1)
print(base64.b64encode(text1))
print(base64.urlsafe_b64encode(text1))

print(text2)
print(base64.b64encode(text2))
print(base64.urlsafe_b64encode(text2))
