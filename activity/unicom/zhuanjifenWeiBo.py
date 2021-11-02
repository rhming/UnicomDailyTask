# -*- coding: utf8 -*-
# import json
import requests
from utils.unicomLogin import UnicomClient
from utils.jifen import encrypt_req_params
from utils import jsonencode as json
from utils.toutiao_sdk import md5
from utils.config import BASE_DIR
from utils.weibo import getCheckToken, rsa_encrypt


class ZJFWeiBo(UnicomClient):

    def __init__(self, mobile, password):
        super(ZJFWeiBo, self).__init__(mobile, password)
        self.session.headers = requests.structures.CaseInsensitiveDict({
            "origin": "https://m.jf.10010.com",
            "user-agent": self.useragent,
            "content-type": "application/json",
            "accept": "*/*",
            "referer": "https://m.jf.10010.com/cms/yuech/unicom-integral-ui/yuech-fl/wbzjf/index.html",
        })
        self.clientVersion = self.version.split('@')[1]
        self.activityId = 'zjfwb'

    def openPlatLineNew(self, to_url, retry=3):
        try:
            url = f'https://m.client.10010.com/mobileService/openPlatform/openPlatLineNew.htm?to_url={to_url}'
            _ = self.session.get(url=url, headers={
                "Origin": "https://img.client.10010.com",
                "X-Requested-With": "com.sinovatech.unicom.ui"
            })
            # print([resp.headers.get('location', '') for resp in _.history])
            if not self.session.cookies.get('_jf_id', ''):
                raise Exception('未获取到_jf_id')
        except Exception as e:
            print(e)
            if retry > 0:
                self.flushTime(5)
                self.openPlatLineNew(to_url, retry - 1)
            else:
                raise Exception("[zhuanjifenWeiBo]获取登录配置失败, 结束执行任务")

    def wbZsLogin(self):
        url = 'https://m.jf.10010.com/jf-yuech/p/wbZsLogin'
        params = {
            'activityId': self.activityId,
            'userCookie': self.session.cookies.get('_jf_id'),
            'userNumber': self.mobile,
        }
        resp = self.session.get(url=url, params=params)
        data = resp.json()
        token = data['data']['token']  # type: dict
        self.session.headers.update({
            "authorization": f"Bearer {token['access_token']}"
        })
        print(data)
        # return data['data']['signCode']
        '''
            giveFlag (0 / 1 / 2)(完成 / 未开始 / 进行中)
        '''
        return data['data'].get('giveFlag', '0'), data['data'].get('signCode', '')

    def giveIntegerRight(self):
        url = 'https://m.jf.10010.com/jf-yuech/api/gameResultV2/giveIntegerRight'
        data = {
            "params": encrypt_req_params(
                {'activityId': 'zjfwb'},
                self.session.cookies.get('_jf_id')
            )
        }
        resp = self.session.post(url=url, json=data)
        resp.encoding = 'utf8'
        data = resp.json()
        print(data)
        try:
            return (data.get('data', {})).get('signCode', '')
        except:
            return ''

    def guestLogin(self, deviceId, androidId):
        url = 'https://api.weibo.cn/2/guest/login'
        params = {
            "networktype": "wifi",
            "launchid": "default",
            # "ul_hid": "uuid4",
            # "ul_sid": uuid4,
            "moduleID": "700",
            "wb_version": "5243",
            "c": "android",
            "ft": "0",
            "ua": "Xiaomi-MI 8 SE__weibo__11.10.0__android__android8.1.0",
            "wm": "20005_0002",
            "v_f": "2",
            "v_p": "89",
            "from": "10BA095010",
            "lang": "zh_CN",
            "skin": "default",
            "oldwm": "20005_0002",
            "sflag": "1",
            "android_id": androidId,
            "ul_ctime": self.timestamp,
            # "cum": "cum",
        }
        data = {
            "device_name": "Xiaomi-MI+8+SE",
            "appkey": "7501641714",
            "checktoken": getCheckToken('', deviceId),
            "preload_ab": "1",
            # "ds": "",
            "did": deviceId[:32],
            "mfp": "01" + rsa_encrypt({
                "1": "Android 8.1.0",
                "2": deviceId,
                "3": deviceId,
                # "4": "imsi",
                "5": self.getMac,
                # "6": "iccid",
                # "7": "ro.serialno",
                "10": androidId,
                "13": "arm64-v8a",
                "14": "MI 8 SE",
                # "15": "getExternalStorageDirectory getTotalBytes",
                # "16": "width*height",
                # "17": "wifi getSSID",
                "22": "Xiaomi",
                "19": "wifi",
                "20": "Xiaomi-MI 8 SE__weibo__11.10.0__android__android8.1.0",
                "50": "1",
                # "51": "getBSSID"
            }),
            "imei": self.getDeviceId,
            "device_id": deviceId,
            "request_ab": "1",
            # "key_hash": "18da2bf10352443a00a5e046d9fca6bd",
            "android_id": androidId,
            "permission_status": "00",
            "packagename": "com.sina.weibo",
        }
        resp = self.session.post(url=url, params=params, data=data, headers={
            'user-agent': 'MI 8 SE_8.1.0_weibo_11.10.0_android',
            "content-type": "application/x-www-form-urlencoded",
        })
        data = resp.json()
        data.update({
            'ab_test': ''
        })
        print(data)
        return data

    def cardList(self, signCode, deviceId, androidId, item):
        url = 'https://api.weibo.cn/2/guest/cardlist'
        params = {
            "networktype": "wifi",
            "extparam": f"from_mobilesign_0940_{signCode}",
            "image_type": "heif",
            "launchid": "10000629-sansiline_shouting_076",
            "uicode": "10000011",
            # "ul_hid": "uuid4",
            # "ul_sid": "uuid4",
            "moduleID": "708",
            "checktoken": getCheckToken(item['uid'], deviceId),
            "wb_version": "5243",
            "card25_new_style": "1",
            "c": "android",
            "s": item['wbsign'],
            "ft": "0",
            "ua": "Xiaomi-MI 8 SE__weibo__11.10.0__android__android8.1.0",
            "wm": "20005_0002",
            "aid": item['aid'],
            "did": deviceId,
            "fid": "102803",
            "uid": item['uid'],
            "v_f": "2",
            "v_p": "89",
            "from": "10BA095010",
            "gsid": item['gsid'],
            "imsi": "",
            "lang": "zh_CN",
            "lfid": "sansiline_shouting_076",
            "page": "1",
            "skin": "default",
            "count": "20",
            "oldwm": "20005_0002",
            "sflag": "1",
            "containerid": "102803",
            "ignore_inturrpted_error": "true",
            "no_location_permission": "1",
            "luicode": "10000629",
            "android_id": androidId,
            "show_layer": "1",
            "need_new_pop": "1",
            "ul_ctime": self.timestamp,
            "need_head_cards": "1",
            # "cum": "cum"
        }

        resp = requests.get(url=url, params=params, headers={
            'user-agent': 'MI 8 SE_8.1.0_weibo_11.10.0_android',
        })
        print(resp.request.headers)
        resp.encoding = 'utf8'
        print(resp.json())

    def run(self):
        to_url = f'https://m.jf.10010.com/jf-order/avoidLogin/forActive/zjytwo&yw_code=&desmobile={self.mobile}&version={self.version}'
        self.openPlatLineNew(to_url)
        giveFlag, signCode = self.wbZsLogin()
        signCode = signCode or self.giveIntegerRight()

        # 一台设备一天只能使用一次
        deviceId = md5(self.mobile) + md5(self.mobile)[::-4]
        androidId = md5(self.mobile)[::-2]
        print(deviceId, androidId)

        item = self.guestLogin(deviceId, androidId)
        item['uid'] = str(item['uid'])
        with open(BASE_DIR + '/utils/wbsign.json', 'r') as fp:
            wbsign = json.loads(fp.read())
        item['wbsign'] = wbsign.get(item['uid'], '')
        if not item['wbsign']:
            return
        if signCode:
            self.cardList(signCode, deviceId, androidId, item)


if __name__ == '__main__':
    pass
