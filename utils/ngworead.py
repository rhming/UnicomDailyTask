# -*- coding: utf8 -*-
from utils.config import BASE_DIR
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad
from hashlib import md5
import base64
import execjs
import json


def auth_sign(appId, timestamp, key='7k1HcDL8RKvc'):
    return md5(''.join([appId, key, str(timestamp)]).encode('utf8')).hexdigest()


def encrypt(plaintext, accesstoken):
    key = accesstoken[16:].encode('utf8')
    iv = '16-Bytes--String'.encode('utf8')
    data = json.dumps(plaintext, ensure_ascii=False, separators=(',', ':',)).encode('utf8')
    data = pad(data, 16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    buf = cipher.encrypt(data).hex().encode('utf8')
    return base64.b64encode(buf).decode('utf8')


def decrypt(ciphertext, accesstoken):
    key = accesstoken[16:].encode('utf8')
    iv = '16-Bytes--String'.encode('utf8')
    data = bytes.fromhex(base64.b64decode(ciphertext).decode('utf8'))
    cipher = AES.new(key, AES.MODE_CBC, iv)
    buf = cipher.decrypt(data)
    buf = unpad(buf, 16)
    return json.loads(buf)


def cryptojs_encrypt(plaintext):
    key = 'null'
    iv = '16-Bytes--String'
    with open(BASE_DIR + '/utils/crypto-js.js', 'r', encoding='utf8') as fp:
        script = fp.read()
    ctx = execjs.compile(script)
    result = ctx.call('encrypt', key, iv, plaintext)
    return result


def cryptojs_decrypt(ciphertext):
    key = 'null'
    iv = '16-Bytes--String'
    with open(BASE_DIR + '/utils/crypto-js.js', 'r', encoding='utf8') as fp:
        script = fp.read()
    ctx = execjs.compile(script)
    result = ctx.call('decrypt', key, iv, ciphertext)
    return result


if __name__ == '__main__':
    pass
