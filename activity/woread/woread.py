# -*- coding: utf8 -*-
# import json
import execjs
import requests
from utils.common import Common
from utils.config import BASE_DIR


class WoRead(Common):

    def __init__(self, mobile, _=None):
        super(WoRead, self).__init__()
        self.mobile = mobile
        self.version = "android@8.0805"
        self.useragent = "Mozilla/5.0 (Linux; Android 8.1.0; MI 8 SE Build/OPM1.171019.019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36; unicom{version:%s,desmobile:%s};devicetype{deviceBrand:Xiaomi,deviceModel:MI 8 SE};{yw_code:}" % (
            self.version,
            self.mobile
        )
        self.session = requests.Session()
        self.session.headers = requests.structures.CaseInsensitiveDict({
            'User-Agent': self.useragent,
            'Origin': 'http://st.woread.com.cn',
            'X-Requested-With': 'XMLHttpRequest'
        })
        cookie = self.readCookie(f'{self.mobile}WoRead')
        if not cookie or not isinstance(cookie, dict):
            cookie = self.CookieStringToDict(cookie)
        self.session.cookies.update(cookie)
        if not self.popupListInfo():
            self.login()

    # def CookieDictToString(self):
    #     return '; '.join(['='.join([k, self.session.cookies.get_dict()[k]]) for k in self.session.cookies.get_dict()])

    def CookieStringToDict(self, cookie):
        return {
            item.split('=', 1)[0]: item.split('=', 1)[1] for item in cookie.split('; ') if item.strip()
        }

    def recordLog(self, log):
        record = self.readCookie(f'{self.mobile}WoReadRecord')
        if not record:
            record = {}
        if not record.get(self.now_date, False):
            if len(record) > 30:
                k = list(record.keys())[0]
                record.pop(k)
            record[self.now_date] = [log]
        else:
            record[self.now_date].append(log)
        self.saveCookie(f'{self.mobile}WoReadRecord', record)

    def getEncryptMobile(self):
        with open(BASE_DIR + '/utils/security.js', 'r', encoding='utf8') as fr:
            securityJs = fr.read()
        scriptText = '''
        function getEncryptMobile(mobile) {
            var modulus = "00A828DB9D028A4B9FC017821C119DFFB8537ECEF7F91D4BC06DB06CC8B4E6B2D0A949B66A86782D23AA5AA847312D91BE07DC1430C1A6F6DE01A3D98474FE4511AAB7E4E709045B61F17D0DC4E34FB4BE0FF32A04E442EEE6B326D97E11AE8F23BF09926BF05AAF65DE34BB90DEBDCEE475D0832B79586B4B02DEED2FC3EA10B3";
            var exponent = "010001";
            var key = window.RSAUtils.getKeyPair(exponent, '', modulus);
            mobile = window.RSAUtils.encryptedString(key, mobile);
            return mobile
        }
        '''
        scriptText = 'var window = {};' + securityJs + scriptText
        ctx = execjs.compile(scriptText)
        EncryptMobile = ctx.call('getEncryptMobile', self.mobile)
        return EncryptMobile

    def login(self):
        self.session.cookies.clear_session_cookies()
        url = 'https://st.woread.com.cn/touchextenernal/common/shouTingLogin.action'
        data = {
            'phonenum': self.getEncryptMobile()
        }
        resp = self.session.post(url=url, data=data)
        print(self.mobile + ' ' + resp.text)
        self.saveCookie(f'{self.mobile}WoRead', self.session.cookies.get_dict())
        if not self.session.cookies.get('useraccount', False):
            raise Exception('[WoRead]登录失败,结束执行任务')

    def popupListInfo(self):
        url = 'https://st.woread.com.cn/touchextenernal/read/popupListInfo.action'
        resp = self.session.post(url=url)
        try:
            resp.json()
            return True
        except:
            return False


if __name__ == '__main__':
    pass
