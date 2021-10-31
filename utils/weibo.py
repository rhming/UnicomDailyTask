# -*- coding: utf8 -*-
import base64
import json
from utils.toutiao_sdk import md5
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey.RSA import importKey


# from Crypto.Random import get_random_bytes


def getCheckToken(userId, deviceId):
    if not userId:
        deviceId = deviceId[0:32]
    return md5(''.join([userId, '/', deviceId, '/', 'obiew']))


def rsa_encrypt(message):
    public_key = '''-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDHHM0Fi2Z6+QYKXqFUX2Cy6AaWq3cPi+GSn9oeAwQbPZR75JB7Netm0HtBVVbtPhzT7UO2p1JhFUKWqrqoYuAjkgMVPmA0sFrQohns5EE44Y86XQopD4ZO+dE5KjUZFE6vrPO3rWW3np2BqlgKpjnYZri6TJApmIpGcQg9/G/3zQIDAQAB\n-----END PUBLIC KEY-----'''
    rsa_key = importKey(public_key)
    cipher = PKCS1_v1_5.new(rsa_key)
    message = json.dumps(message, separators=(',', ':',), ensure_ascii=False).encode('utf8')
    length = len(message)
    num = length // 117 + 1 if length % 117 else length // 117
    buf = b''
    for index in range(num):
        start = index * 117
        end = start + 117 if length > start + 117 else length
        buf += cipher.encrypt(message[start:end])
    return base64.b64encode(buf).decode('utf8')


# def rsa_decrypt(ciphertext):
#     private_key = '-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----'
#     rsa_key = importKey(private_key)
#     sentinel = get_random_bytes(16)
#     cipher = PKCS1_v1_5.new(rsa_key)
#     ciphertext = base64.b64decode(ciphertext)
#     length = len(ciphertext)
#     num = length // 256 + 1 if length % 256 else length // 256
#     buf = b''
#     for index in range(num):
#         start = index * 256
#         end = start + 256 if length > start + 256 else length
#         print(start, end)
#         buf += cipher.decrypt(ciphertext[start:end], sentinel)  # type: bytearray
#     return buf.decode('utf8')


if __name__ == '__main__':
    pass
