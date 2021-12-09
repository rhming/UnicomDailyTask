# -*- coding: utf8 -*-
import time
from threading import Thread
from activity.unicom.dailySign import SigninApp
from activity.unicom.integralTask import IntegralTask
from activity.unicom.watchAddFlow import WatchAddFlow
from activity.unicom.watchAddFee import WatchAddFee
from activity.unicom.superSimpleTask import SuperSimpleTask
from activity.unicom.unicomTurnCard import TurnCard
from activity.unicom.unicomTurnTable import TurnTable
from activity.unicom.unicomZhuaWaWa import ZhuaWaWa
from activity.unicom.sheggMachine import SheggMachine
from activity.unicom.blindBox import BlindBox
from activity.unicom.unicomSignerTask import SignerTask
from activity.unicom.zhuanjifenWeiBo import ZJFWeiBo
from activity.unicom.qiandao11 import QianDao11
from activity.woread.luckdraw import LuckDraw
from activity.woread.openbook import OpenBook
from activity.woread.readluchdraw import ReadLuchDraw
from activity.woread.thanksgiving import ThanksGiving
from activity.woread.prizedetail import Prize
from activity.wolearn.zsmh import ZSMHAct
from activity.wolearn.xxdgg import XxdggAct
from activity.wolearn.wabao import WzsbzAct
from activity.wolearn.wmms2 import BxwmAct
from activity.wolearn.stdt5 import Stdthd
from activity.womail.dailyTask import DailySign
from activity.womail.webmail import WoMailWeb
# from activity.womail.scratchable import Scratchable
# from activity.womail.puzzle2 import Puzzle2
from activity.womusic.womusic import WoMusic
from activity.womusic.dayDayDraw import DayDayDraw
from activity.push.pushlog import PushLog


def Template(cls):
    # 联通手机号 服务密码 配置 (支持多账号)
    ts = []
    for mobile, password in [
        # ('手机号', '服务密码'),
        # ('手机号', '服务密码'),
    ]:
        ts.append(Thread(target=cls(mobile, password).run))
    for t in ts:
        t.start()
    for t in ts:
        t.join()


def WebMailTemplate(cls):
    # 网页版沃邮箱签到活动
    # https://mail.wo.cn 网页版沃邮箱账号密码 只需填写手机号 不需加后缀@wo.cn
    ts = []
    for mobile, password in [
        # ('手机号', '密码'),
        # ('手机号', '密码'),
    ]:
        ts.append(Thread(target=cls(mobile, password).run))
    for t in ts:
        t.start()
    for t in ts:
        t.join()


def WXTemplate(cls):
    # 微信沃邮箱 mobile openId配置 (支持多账号)
    ts = []
    for item in [
        # {
        #     "mobile": "xxx",
        #     "openId": "xxx"
        # },
        # {
        #     "mobile": "xxx",
        #     "openId": "xxx"
        # },
    ]:
        ts.append(Thread(target=cls(**item).run))
    for t in ts:
        t.start()
    for t in ts:
        t.join()


def PushTemplate():
    # 消息推送 (读取数据存储服务记录的日志进行推送)
    # utils/config.py 推送配置
    # 填写参与活动任务的账号
    # 不需要推送 可以不填
    PushLog([
        # "联通手机号-1",
        # "联通手机号-2",
        # "沃邮箱mobile-1",
        # "沃邮箱mobile-2",
    ]).run()


def main_handler(event=None, context=None):
    """
        腾讯云函数每15分钟执行一次
    """
    now_time = int(time.strftime(
        '%H%M',
        time.localtime(time.time() + 8 * 60 * 60 + time.timezone)
    ))
    DEBUG = False
    # 沃阅读活动
    if now_time in range(600, 800) or DEBUG:  # 7次
        Template(LuckDraw)
        Template(OpenBook)
    if now_time in range(600, 730) or DEBUG:  # 5次
        Template(ThanksGiving)
    if now_time in range(800, 830) or DEBUG:  # 1次
        Template(ReadLuchDraw)
    if now_time in range(830, 900) or DEBUG:  # 自动领取奖品
        Template(Prize)

    # 沃学习活动
    if now_time in range(900, 1100) or DEBUG:
        Template(ZSMHAct)  # 7
        Template(XxdggAct)  # 8
        Template(WzsbzAct)  # 6
        Template(BxwmAct)  # 5
    if now_time in range(900, 930) or DEBUG:
        Template(Stdthd)

    # 沃邮箱活动
    if now_time in range(1000, 1010) or now_time in range(1300, 1310) or DEBUG:
        WXTemplate(DailySign)
        WebMailTemplate(WoMailWeb)
        # WXTemplate(Puzzle2)
        # WXTemplate(Scratchable)

    # ----------------------------------------------------------------
    # 使用华为云函数工作流 (腾讯云函数、阿里函数计算 ip在获取积分接口被限制)
    # 联通每日签到
    if now_time in range(800, 830) or now_time in range(1130, 1200) or now_time in range(1530, 1600) or DEBUG:
        Template(SigninApp)
        Template(WatchAddFee)

    # 联通签到页看视频领流量
    if now_time in range(800, 900) or DEBUG:
        Template(WatchAddFlow)

    # 赚积分外卖购物任务
    if now_time in range(900, 930) or DEBUG:
        Template(SignerTask)
        Template(ZJFWeiBo)
        Template(QianDao11)
        Template(WoMusic)
        Template(DayDayDraw)

    # 联通签到页积分任务
    if now_time in range(800, 1600) or DEBUG:
        Template(SuperSimpleTask)

    # 联通积分翻倍任务
    if now_time in range(800, 1000) or DEBUG:
        Template(IntegralTask)

    # 联通签到页转盘抽卡任务
    if now_time in range(900, 1100) or DEBUG:
        Template(SheggMachine)
        Template(BlindBox)
        Template(TurnCard)
        Template(TurnTable)
        Template(ZhuaWaWa)

    # 消息推送
    if now_time in range(1130, 1140) or now_time in range(1530, 1540) or DEBUG:
        PushTemplate()
