# -*- coding: utf8 -*-
import re
# import json
from lxml import etree
from utils.config import BASE_DIR
from utils import jsonencode as json
from urllib.parse import quote, urlencode
from activity.woread.flowdraw import WoRead


class Prize(WoRead):

    def __init__(self, mobile, _=None):
        super(Prize, self).__init__(mobile)
        self.session.headers.update({
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Referer": "http://st.woread.com.cn/touchextenernal/read/myPrize.action?type=2"
        })
        self.addrInfo = None

    def queryParamToDict(self, value):
        return {
            item.split('=', 1)[0]: item.split('=', 1)[1] for item in value.split('&') if item.strip()
        }

    def updateAddr(self, item):
        self.session.headers.update({
            "Referer": "http://st.woread.com.cn" + item['url'].replace("index.action", "add.action")
        })
        url = 'http://st.woread.com.cn/touchactivity/deliveryaddress/updateUserAddr.action'
        data = {
            "addrid": "",
            "userid": item['userid'],
            "token": item['token'],
            "contatcphone": self.mobile
        }
        with open(BASE_DIR + '/utils/address.json', 'r', encoding='utf8') as fp:
            info = json.loads(fp.read())
        if info.get(self.mobile, False):
            data.update(info[self.mobile])
            print(data)
            resp = self.session.post(url=url, data=data)
            resp.encoding = 'utf8'
            print(resp.text)
        else:
            raise Exception("未获取到配置信息,创建收货地址失败")

    def index(self, item, retry=1):
        url = 'http://st.woread.com.cn' + item['url']
        resp = self.session.get(url=url)
        resp.encoding = 'utf8'
        if resp.text.find('itemCenter') > -1:
            print('收货地址存在')
            e = etree.HTML(resp.text)
            info = e.xpath('string(//div[@class="itemCenter"]/@onclick)')
            self.addrInfo = json.loads(
                re.sub(r'selectAddress\((\{.+\}).+', r'\1', info)
            )
            print(self.addrInfo)
        else:
            print('收货地址不存在')
            if retry > 0:
                self.updateAddr(item)
                self.index(item, retry - 1)

    def parsePrize(self):
        url = 'http://st.woread.com.cn/touchextenernal/read/moreMyPrize.action'
        data = {
            "curpage": "1",
            "limit": "20"
        }
        resp = self.session.post(url=url, data=data)
        resp.encoding = 'utf8'
        e = etree.HTML(resp.text)
        prizeList = [
            re.sub(r"jump\('(.+)'\)", r'\1', item) for item in e.xpath('//div[@class="confirm_btn"]/@onclick')
        ]
        prizeNameList = [
            ele.xpath('normalize-space(.)')
            for ele in e.xpath('//div[@class="mpCell flex f-between f-align"]')
            if ele.xpath('.//div[@class="confirm_btn"]')
        ]
        return prizeList, prizeNameList

    def getPrize(self, item):
        self.session.headers.update({
            "Referer": "http://st.woread.com.cn" + item['url']
        })
        url = 'http://st.woread.com.cn/touchactivity/deliveryaddress/updateUserReceivingAddress.action'
        data = self.addrInfo
        data.update({
            "userid": item['userid'],
            "token": item['token'],
            "datetime": item['datetime'].replace(' ', '+'),
            "activeindex": item['activityindex'],
            "prizeindex": item['prizeindex']
        })
        data = urlencode(data, safe='+').encode('utf8')
        resp = self.session.post(url=url, data=data)
        resp.encoding = 'utf8'
        print(resp.text)

    def run(self):
        for index, (prize, name) in enumerate(zip(*self.parsePrize())):
            print(prize)
            print(name)
            item = self.queryParamToDict(prize.split('?')[1])
            item['url'] = quote(prize, safe='/=&:?')
            if index == 0:
                self.index(item)
            if not self.addrInfo:
                return
            self.getPrize(item)
            self.flushTime(3)


if __name__ == '__main__':
    pass
