# -*- coding: utf8 -*-
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from utils.toutiao_sdk import md5


def encrypt_params(value):
    if not isinstance(value, bytes):
        data = str(value).encode('utf8')
    cipher = AES.new(
        key="1bd83b249a414036".encode('utf8'),
        mode=AES.MODE_CBC,
        iv="16-Bytes--String".encode('utf8')
    )
    data = cipher.encrypt(pad(data, 16))
    return base64.b64encode(data).decode('utf8')


def sign(timestamp):
    data = f'{timestamp}VNEU8G4V'
    return md5(data).upper()


if __name__ == '__main__':
    pass
