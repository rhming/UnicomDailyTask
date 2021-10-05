# -*- coding: utf8 -*-
import math
import json
import base64
from random import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import ARC4


def secretkeyArray():
    keyArr = []
    chars = [
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
        'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f',
        'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
    ]
    for i in range(5):
        nums = ""
        for j in range(16):
            id_ = math.floor(random() * 62)
            nums += chars[id_]
        keyArr.append(nums)
    return keyArr


def encrypt_free_login_params(params):
    keyArr = secretkeyArray()
    keyrdm = math.floor(random() * 5)
    key = keyArr[keyrdm]
    data = json.dumps(params, separators=(',', ':',), ensure_ascii=False).encode('utf8')
    data = pad(data, 16)
    cipher = AES.new(key=key.encode('utf8'), mode=AES.MODE_ECB)
    buf = cipher.encrypt(data)
    return {
        "params": base64.b64encode(buf).decode('utf8') + str(keyrdm),
        "parKey": keyArr
    }


def decrypt_free_login_params(ciphertext):
    keyArr = ciphertext['parKey']
    keyrdm = int(ciphertext['params'][-1])
    key = keyArr[keyrdm]
    data = ciphertext['params'][:-1]
    data = base64.b64decode(data)
    cipher = AES.new(key=key.encode('utf8'), mode=AES.MODE_ECB)
    buf = cipher.decrypt(data)
    buf = unpad(buf, 16)
    return json.loads(buf)


def encrypt_req_params(params, jfid):
    data = json.dumps(params, separators=(',', ':',), ensure_ascii=False).encode('utf8')
    key = jfid[3:19]
    cipher = ARC4.new(key=key.encode('utf8'))
    buf = cipher.encrypt(data)
    return base64.b64encode(buf).decode('utf8')


def decrypt_req_parmas(ciphertext, jfid):
    data = base64.b64decode(ciphertext)
    key = jfid[3:19]
    cipher = ARC4.new(key=key.encode('utf8'))
    buf = cipher.decrypt(data)
    return json.loads(buf)


if __name__ == '__main__':
    ciphertext = 'vVrTBH9LyYJQ/NziU6ekQpioCmfgBboeYjZL18iButoqqLGEBBAsZpWSwcUIXIrtk66O40sEpAdT7RY8uHdPVcoOTDtF9O+mYcnCXt5W49X+4RtjMg=='
    jfid = 'sc7bwje3f9aa0c9ce2414f3cb503c7daa21d33b3uswadtwu'
    params = decrypt_req_parmas(ciphertext, jfid)
    print(params)
    data = encrypt_req_params(params, jfid)
    print(data)
    params = {
        'params': 'vnlPS76bsYVuMYXa0AM4F8C2ltJShkVxOBQlAAsSD29M3pzyYz+QUqcBKlz9qAwi5do40Boo7BYHf9ulrESoEXo5o4gErEWIYromZnBft8vf1Calz/ROLj93Knlz44T39ed6EF4f7SpO7+cXMEbEIkgzli/q+B9fFY+ys6eHefw=3',
        'parKey': ['6AJ1cxGTlGirbqfy', 'slnLthFmSxz3eHSL', 'VORCJTc0nDh41R17', 'M99BXj5MMyVsFdLh', 'PseUfSmw4YYhzvNx']
    }
    data = decrypt_free_login_params(params)
    print(data)
    data = encrypt_free_login_params(data)
    print(data)
