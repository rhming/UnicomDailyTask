import time
import json
import base64
import hashlib
# import datetime
from Crypto.Cipher import AES


def md5(data):
    if not isinstance(data, bytes):
        data = str(data).encode('utf8')
    cipher = hashlib.md5()
    cipher.update(data)
    data = cipher.hexdigest()
    return data


def getSign(options):
    secret = 'integralofficial&'
    value = secret + '&'.join([
        f'{k}{options[k]}' for k in options if k.find('arguments') > -1 and options.get(k, '').strip()
    ])
    return md5(value)


def create_key_iv():
    timestamp = str(time.time() + 8 * 60 * 60)
    key = (md5(timestamp) * 2)[16:48]
    iv = (md5(key) * 2)[8:24]
    return key, iv


def cbc_encrypt(data, key, iv):
    data = json.dumps(
        data,
        separators=(',', ':',),
        ensure_ascii=False
    ).replace('/', '\\/').encode('utf8')
    cipher = AES.new(
        key.encode('utf8'),
        mode=AES.MODE_CBC,
        iv=iv.encode('utf8')
    )
    length = (16 - len(data) % 16) % 16
    data += (length.to_bytes(1, 'big') * length)
    data = cipher.encrypt(data)
    data = base64.b64encode(data).decode('utf8')
    data = ''.join([
        f'{c}\n' if i % 76 == 0 else c for i, c in enumerate(data, 1)
    ])
    return '3' + (key * 2)[16:48] + iv + data


def cbc_decrypt(message):
    key = (message[1:33] * 2)[16:48]
    iv = message[33:49]
    data = message[49:].replace('\n', '')
    cipher = AES.new(
        key.encode('utf8'),
        mode=AES.MODE_CBC,
        iv=iv.encode('utf8')
    )
    data = base64.b64decode(data)
    length = (16 - len(data) % 16) % 16
    data += (length.to_bytes(1, 'big') * length)
    data = cipher.decrypt(data)
    data = data[:-data[-1]]
    data = json.loads(data)
    return data


if __name__ == '__main__':
    pass
