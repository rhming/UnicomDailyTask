# -*- coding: utf8 -*-
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def encrypt_mobile(mobile):
    cipher = AES.new(key='gb6YCccUvth75Tm2'.encode('utf8'), mode=AES.MODE_ECB)
    buf = cipher.encrypt(pad(mobile.encode('utf8'), 16))
    return base64.b64encode(buf).decode('utf8')


def decrypt_mobile(mobile):
    cipher = AES.new(key='gb6YCccUvth75Tm2'.encode('utf8'), mode=AES.MODE_ECB)
    data = base64.b64decode(mobile)
    data = cipher.decrypt(data)
    data = unpad(data, 16).decode('utf8')
    return data


if __name__ == '__main__':
    pass
