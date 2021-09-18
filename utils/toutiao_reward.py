import requests
from uuid import uuid4
from urllib.parse import quote
from utils.common import Common
from random import randint, random
from utils.toutiao_sdk import cbc_encrypt, cbc_decrypt, create_key_iv, md5


class TouTiao(Common):

    def __init__(self, mobile):
        super(TouTiao, self).__init__()
        self.mobile = mobile
        self.session = requests.Session()
        self.session.headers = requests.structures.CaseInsensitiveDict({
            "content-type": "application/json; charset=utf-8",
            "accept-encoding": "gzip",
            "user-agent": "okhttp/3.9.1",
        })

    def reward(self, options):
        orderId = md5(str(self.timestamp) + self.mobile)
        print(orderId)
        media_extra = [
            options.get('ecs_token', ''),
            self.mobile,
            'android',
            options.get('arguments1', ''),
            options.get('arguments2', ''),
            orderId,
            str(options.get('codeId', '')),
            options.get('channelName', '') or options.get('remark', ''),
            '4G'
        ]
        duration = randint(28000, 30000) / 1000
        message = {
            "oversea_version_type": 0,
            "reward_name": f"android-{options['remark']}-激励视频",
            "reward_amount": 1,
            "network": 5,
            "sdk_version": "3.6.1.4",
            "user_agent": "Mozilla/5.0 (Linux; Android 8.1.0; MI 8 SE Build/OPM1.171019.019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36",
            "extra": {
                "ad_slot_type": 7,
                "oaid": "",
                "language": "golang",
                "ug_creative_id": "",
                "ad_id": None,
                "creative_id": None,
                "convert_id": None,
                "uid": None,
                "ad_type": None,
                "pricing": None,
                "ut": 12,
                "version_code": "8.8.5",
                "device_id": None,
                "width": 360,
                "height": 705,
                "mac": "00:00:00:00:00:00",
                "uuid": "",
                "uuid_md5": "d41d8cd98f00b204e9800998ecf8427e",
                "os": "android",
                "client_ip": "",
                "open_udid": "",
                "os_type": None,
                "app_name": "中国联通APP",
                "device_type": "MI 8 SE",
                "os_version": "8.1.0",
                "app_id": "5049584",
                "template_id": 0,
                "template_rate": 0,
                "promotion_type": 0,
                "img_gen_type": 0,
                "img_md5": "",
                "source_type": None,
                "pack_time": round(self.timestamp / 1000 + random(), 6),
                "cid": None,
                "interaction_type": 3,
                "src_type": "app",
                "package_name": "com.sinovatech.unicom.ui",
                "pos": 5,
                "landing_type": None,
                "is_sdk": True,
                "is_dsp_ad": None,
                "imei": "",
                "req_id": "",
                "rit": int(options.get('codeId', 0)),
                "vid": "",
                "orit": 900000000,
                "ad_price": "",
                "shadow_ad_id": None,
                "shadow_creative_id": None,
                "shadow_advertiser_id": None,
                "shadow_campaign_id": None,
                "dynamic_ptpl_id": None,
                "engine_external_url": "",
                "engine_web_url": "",
                "variation_id": "",
                "app_bundle_id": "com.sinovatech.unicom.ui",
                "applog_did": "",
                "ad_site_id": "",
                "ad_site_type": 1,
                "clickid": "",
                "global_did": None,
                "ip": "",
                "ua": "Mozilla/5.0 (Linux; Android 8.1.0; MI 8 SE Build/OPM1.171019.019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36",
                "sys_language": "zh-CN",
                "playable_var_ids": "",
                "playable_template_var_id": 0,
                "country_id": None,
                "province_id": None,
                "city_id": None,
                "dma_id": None,
                "playable_url": None,
                "dco_pl_strategy": None,
                "dy_pl_type": None
            },
            "media_extra": quote('|'.join(media_extra)),
            "video_duration": duration,
            "play_start_ts": int(self.timestamp / 1000) - randint(30, 35),
            "play_end_ts": 0,
            "duration": int(duration * 1000),
            "user_id": "5049584",
            "trans_id": uuid4().hex,
            "latitude": 0,
            "longitude": 0
        }
        key, iv = create_key_iv()
        message = cbc_encrypt(message, key, iv)
        data = {
            'message': message,
            'cypher': 3
        }
        url = 'https://api-access.pangolin-sdk-toutiao.com/api/ad/union/sdk/reward_video/reward/'
        resp = self.session.post(url=url, json=data)
        resp.encoding = 'utf8'
        data = resp.json()
        if data.get('message', False):
            try:
                message = cbc_decrypt(data['message'])
                print(message)
            except:
                pass
        print(data)
        return orderId


if __name__ == '__main__':
    pass
