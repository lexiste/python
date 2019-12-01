
## need to use python2 and not python3
from Crypto.PublicKey import RSA
code = 'securityisagoodthing'
key = RSA.generate(4069)
encrypted_key = key.exportKey(passphrase=code, pkcs=8, protection="scryptAndAES128-CBC")
with open('/root/pentest/rsaKey.bin', 'wb') as f:
        f.write(encrypted_key)
with open('/root/pentest/rsaKey.pem', 'wb') as f:
        f.write(key.publickey().exportKey())

print('created RSA keys in /root/pentest/rsaKey with passphrase %s' % (code))
