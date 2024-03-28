# AES SHELLCODE ENCRYPTION 

import sys
import os
from Crypto.Cipher import AES
from os import urandom
import hashlib

KEY = urandom(16)

def pad(s):
    block_size = AES.block_size
    padding = block_size - len(s) % block_size
    return s + bytes([padding] * padding)


def aesenc(plaintext, key):
    k = hashlib.sha256(key).digest()
    iv = bytes(16)
    plaintext = pad(plaintext)
    cipher = AES.new(k, AES.MODE_CBC, iv)

    return cipher.encrypt(plaintext)


try:
    plaintext = open(sys.argv[1], "rb").read()
except:
    print("File argument needed! %s <raw payload file>" % sys.argv[0])
    sys.exit()

ciphertext = aesenc(plaintext, KEY)

#print('payload[] = { 0x' + ', 0x'.join(hex(ord(x))[2:] for x in ciphertext) + ' };')
print('char key[] = { ' + ', '.join('0x{:02x}'.format(b) for b in bytearray(KEY)) + ' };')

print('unsigned char payload[] = { ' + ', '.join('0x{:02x}'.format(b) for b in ciphertext) + ' };')

open("shellcode.aes", "wb").write(ciphertext)
