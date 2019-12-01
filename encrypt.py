
## need to use python2 and not python3
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

outputFile = '/root/tmp/test-file.txt'

with open(outputFile, 'wb') as out_file:
    ## the .pem file is the public portion of our key, use it to encrypt messages
    recipient_key = RSA.import_key(open('/root/pentest/rsaKey.pem').read())
    session_key = get_random_bytes(16)

    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    out_file.write(cipher_rsa.encrypt(session_key))

    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    data = b'this is some random test data'
    ciphertext, tag = cipher_aes.encrypt_and_digest(data)

    out_file.write(cipher_aes.nonce)
    out_file.write(tag)
    out_file.write(ciphertext)

print('created encrypted file %s' % outputFile)
