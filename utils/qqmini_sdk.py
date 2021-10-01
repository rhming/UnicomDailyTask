# -*- coding: utf8 -*-
import hmac
import base64
from hashlib import sha256
from urllib.parse import quote


def HmacSHA256(data, key='test'):
    key = key.encode('utf8')
    message = data.encode('utf8')
    sign = base64.b64encode(hmac.new(key, message, digestmod=sha256).digest())
    sign = sign.decode('utf8')
    return quote(sign)


if __name__ == '__main__':
    pass
