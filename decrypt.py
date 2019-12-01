
## need to use python2 and not python3
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP

code = 'securityisagoodthing'
inputFile = '/root/tmp/test-file.txt'

with open(inputFile, 'rb') as fObj:
    ## the .bin file is the private portion of our key, use it to decrypt messages
    private_key = RSA.import_key(open('/root/pentest/rsaKey.bin').read(), passphrase=code)
    enc_session_key, nonce, tag, ciphertext = [ fObj.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1) ]

    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)

    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext, tag)

print(data)
