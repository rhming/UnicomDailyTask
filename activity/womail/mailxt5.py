# -*- coding: utf8 -*-
import re
import requests
from utils.common import Common
from utils.bol import rsa_encrypt_password
from lxml import etree


class XT5CoreMail(Common):

    def __init__(self, mobile, password):
        super(XT5CoreMail, self).__init__()
        self.mobile = mobile
        self.password = password
        self.session = requests.Session()
        self.session.headers = requests.structures.CaseInsensitiveDict({
            "Referer": "https://mail.wo.cn/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
        })

    def getSid(self):
        url = 'https://mail.wo.cn/'
        resp = self.session.get(url)
        text = resp.text
        result = re.findall(r'&sid=([^"]+)', text)
        self.session.cookies.update({
            'uid': f'{self.mobile}%40wo.cn'
        })
        if result:
            return result[0]
        return ''

    def getTempSession(self):
        url = 'https://mail.wo.cn/coremail/s/?func=user:getTempSession'
        resp = self.session.post(url=url)
        text = resp.content
        try:
            return etree.HTML(text).xpath('string(//object[@name="var"]/string[@name="sid"])')
        except:
            return ''

    def getPasswordKey(self):
        # sid = self.getTempSession()
        sid = self.getSid()
        # url = f'https://mail.wo.cn/coremail/s/?func=user:getPasswordKey&sid={sid}'
        url = f'https://mail.wo.cn/coremail/s/json?sid={sid}&func=user:getPasswordKey'
        resp = self.session.post(url=url)
        data = resp.json()

        # try:
        #     return (
        #         etree.HTML(text).xpath('string(//object[@name="var"]/string[@name="sid"])'),
        #         {
        #             'type': etree.HTML(text).xpath('string(//object[@name="key"]/string[@name="type"])'),
        #             'e': etree.HTML(text).xpath('string(//object[@name="key"]/string[@name="e"])'),
        #             'n': etree.HTML(text).xpath('string(//object[@name="key"]/string[@name="n"])')
        #         }
        #     )
        # except:
        #     return '', {}
        return data.get('var', {}).get('sid', ''), data.get('var', {}).get('key', {})

    def login(self):
        sid, key = self.getPasswordKey()
        url = f'https://mail.wo.cn/coremail/index.jsp?cus=1&sid={sid}'
        data = {

            'locale': 'zh_CN',
            'nodetect': 'false',
            'destURL': '',
            'supportLoginDevice': 'true',
            'accessToken': '',
            'timestamp': '',
            'signature': '',
            'nonce': '',
            'device': '{"uuid":"webmail_windows","imie":"webmail_windows","friendlyName":"chrome 95","model":"windows","os":"windows","osLanguage":"zh-CN","deviceType":"Webmail"}',
            'supportDynamicPwd': 'true',
            'supportBind2FA': 'true',
            'authorizeDevice': '',
            'loginType': '',
            'uid': self.mobile,
            'domain': '',
            'password': rsa_encrypt_password(self.password, key),
            'action:login': ''
        }
        resp = self.session.post(url=url, data=data)
        print(resp.text)

    def cmcuLogin(self, sid, key):
        timestamp = self.timestamp
        url = f'https://mail.wo.cn/coremail/s/?func=cmcu:login&sid={sid}'
        data = {
            "uid": f"{self.mobile}@wo.cn",
            "password": rsa_encrypt_password(self.password, key),
            "locale": "zh_CN",
            "supportDynamicPwd": True,
            "supportSms": True,
            "device": {
                "uuid": f"hxphone_{timestamp}",
                "model": "android",
                "os": "android",
                "imie": f"hxphone_{timestamp}",
                "friendlyName": "na",
                "osLanguage": "zh-CN",
                "deviceType": "Hxphone"
            }
        }
        resp = self.session.post(url=url, json=data, headers={
            'Content-Type': 'text/x-json',
            'Origin': 'https://mail.wo.cn',
            'Referer': 'https://mail.wo.cn/coremail/hxphone/',
            'X-CM-SERVICE': 'PHONE'
        })
        print(resp.text)

    def userLogin(self, sid, key):
        timestamp = self.timestamp
        url = f'https://mail.wo.cn/coremail/s/?func=user:login&sid={sid}'
        data = {
            "uid": f"{self.mobile}@wo.cn",
            "password": rsa_encrypt_password(self.password, key),
            "locale": "zh_CN",
            "supportDynamicPwd": True,
            "supportSms": True,
            "device": {
                "uuid": f"hxphone_{timestamp}",
                "model": "android",
                "os": "android",
                "imie": f"hxphone_{timestamp}",
                "friendlyName": "na",
                "osLanguage": "zh-CN",
                "deviceType": "Hxphone"
            }
        }
        resp = self.session.post(url=url, json=data, headers={
            'Content-Type': 'text/x-json',
            'Origin': 'https://mail.wo.cn',
            'Referer': 'https://mail.wo.cn/coremail/hxphone/',
            'X-CM-SERVICE': 'PHONE'
        })
        text = resp.content
        print(text)
        try:
            return {
                'sid': etree.HTML(text).xpath('string(//object[@name="var"]/string[@name="sid"])'),
                'uid': etree.HTML(text).xpath('string(//object[@name="var"]/string[@name="uid"])'),
                'primaryEmail': etree.HTML(text).xpath('string(//object[@name="var"]/string[@name="primaryEmail"])'),
                'accessToken': etree.HTML(text).xpath('string(//object[@name="var"]/string[@name="accessToken"])'),
                'accessSecret': etree.HTML(text).xpath('string(//object[@name="var"]/string[@name="accessSecret"])'),
                'nonce': etree.HTML(text).xpath('string(//object[@name="var"]/string[@name="nonce"])'),
            }
        except:
            return {
                'sid': '',
                'uid': '',
                'primaryEmail': '',
                'accessToken': '',
                'accessSecret': '',
                'nonce': '',
            }

    # def getSocketSid(self, sid):
    #     url = 'https://mail.wo.cn/socket.io/?EIO=3&transport=polling&t='
    #     resp = self.session.get(url=url, headers={
    #         'Origin': 'https://mail.wo.cn',
    #         'Referer': 'https://mail.wo.cn/coremail/hxphone/',
    #         'X-CM-SERVICE': 'PHONE'
    #     })
    #     print(resp.content)
    #
    # def _(self, sid, ssid):
    #     url = f'https://mail.wo.cn/socket.io/?EIO=3&transport=polling&t=&sid={ssid}'
    #     resp = self.session.post(
    #         url=url,
    #         data='138:42["auth",{"clientId":"webmail:%s","sid":"%s","username":"%s@wo.cn"}]' % (
    #             sid,
    #             sid,
    #             self.mobile
    #         ),
    #         headers={
    #             'Content-Type': 'text/plain;charset=UTF-8',
    #             'Origin': 'https://mail.wo.cn',
    #             'Referer': 'https://mail.wo.cn/coremail/hxphone/',
    #             'X-CM-SERVICE': 'PHONE'
    #         }
    #     )
    #     print(resp.content)

    def run(self):
        self.login()


if __name__ == '__main__':
    pass
