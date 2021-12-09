# -*- coding: utf8 -*-
from Crypto.Cipher import AES
from Crypto.PublicKey.RSA import importKey, RsaKey
from Crypto.Cipher import PKCS1_v1_5
import base64


def encrypt_password(password):
    if not isinstance(password, bytes):
        password = str(password).encode('utf8')
    length = len(password)
    password = password + (16 - length % 16) % 16 * b'\x00'
    cipher = AES.new(key=b'72VqcqjdqTO6QDH5', iv=b'72VqcqjdqTO6QDH5', mode=AES.MODE_CBC)
    buf = cipher.encrypt(password)
    result = base64.b64encode(buf).decode('utf8')
    return result


def hex_string_to_int(string):
    if len(string) % 2:
        string = '0' + string
    return int.from_bytes(bytes.fromhex(string), 'big')


def rsa_encrypt_password(password, key):
    if not isinstance(password, bytes):
        password = str(password).encode('utf8')
    rsa_key = importKey(RsaKey(e=hex_string_to_int(key['e']), n=hex_string_to_int(key['n'])).exportKey())
    cipher = PKCS1_v1_5.new(rsa_key)
    return cipher.encrypt(password).hex()


if __name__ == '__main__':
    pass
