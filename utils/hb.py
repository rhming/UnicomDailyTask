# -*- coding: utf8 -*-
import re
import math
import time
import random
from hashlib import sha1
from urllib.parse import quote

heartbeatKey = '189a98bc908d889a'  # '128a7bc09874c0d8'


def MathRand():
    Num = ""
    for _ in range(6):
        Num += f"{math.floor(random.random() * 10)}"
    return Num


def heartbeat(newid, gid, stl_id):
    timestamp = f"{int(time.time() + 8 * 60 * 60)}"
    r = MathRand()
    arr = []
    arr.append(newid)
    arr.append(gid)
    arr.append(stl_id)
    arr.append(timestamp)
    arr.append(r)
    arr.append(heartbeatKey)

    temparr = sorted(arr)
    tempstr = ''.join(temparr)
    sign = sha1(tempstr.encode('utf8')).hexdigest()
    return sign, r, timestamp


def getUrlParam(url, name):
    # url = "http://assistant.flow.wostore.cn/?ct=h5quicklogin&gid=2899&xw_flow=0&xw_lt=1&xw_lc=2&member=302"
    param = re.sub(r'.+' + name + r'=([^&]*).*', r'\1', url)
    return quote(param, safe='')
