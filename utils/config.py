import os
import base64

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')

# 设备ID(通常是获取手机的imei) 联通判断是否登录多台设备 不能多台设备同时登录 填写常用的设备ID
deviceIds = {
    'mobile-1': 'imei-1',
    'mobile-2': 'imei-2',
}

# 数据存储接口
data_storage_server_url = ''  # https://utf8.pythonanywhere.com/

# 数据存储接口授权配置
username = ''  # 账户
password = ''  # 密码
Authorization = 'Basic ' + base64.b64encode(
    ':'.join([username, password]).encode('utf8')
).decode('utf8')

# 消息推送配置
push_message_conf = {
    # qq邮箱推送
    "qq": {
        "msg_from": "",  # 发送人qq邮箱
        "password": "",  # 发送人qq邮箱的授权码
        "msg_to": "",  # 收件人邮箱 (发送人和接收人可以相同)
    },
    # pushplus(微信公众号接收消息推送) http://www.pushplus.plus/
    "pushplus": {
        "token": "",  # pushplus消息推送token,
    },
    # tg-bot推送 参考文档 https://core.telegram.org/bots/api#sendmessage
    # 用户id、频道id获取 (需与bot建立会话) 参考文档 https://core.telegram.org/bots/api#getupdates
    # tg_api 推荐使用cloudflare免费创建workers程序转发 https://dash.cloudflare.com/ 或 其它反向代理 转发
    "tg": {
        "bot_token": "",  # 机器人token
        "chat_id": "",  # 用户id、频道id、频道名 (t.me/<频道名>)
        "tg_api": "",  # tg转发api
    },
    # server酱推送 参考文档 https://sct.ftqq.com/sendkey api参数详细说明
    # 需在server酱 配置消息通道 默认微信方糖公众号接收
    # channel 方糖服务号=9、Android=98、Bark iOS=8、企业微信群机器人=1、钉钉群机器人=2、飞书群机器人=3、测试号=0、自定义=88、企业微信应用消息=66
    "ftqq": {
        "sendkey": "",  # server酱 SendKey
        "channel": "",  # 指定消息通道 选填 最多可选两个 以`|`分割 例如: 1|2
        "openid": "",  # 消息抄送的openid 选填 企业微信群中成员账号名
    }
}
