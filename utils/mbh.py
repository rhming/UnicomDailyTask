# -*- coding: utf8 -*-
from random import randint
from hashlib import md5


def gztoken(mobile, timestamp):
    return md5(f"{mobile}dncj@2181{timestamp}spamx1a7s".encode('utf8')).hexdigest().upper()


def random():
    return randint(0, 10 ** 8)


if __name__ == '__main__':
    pass
