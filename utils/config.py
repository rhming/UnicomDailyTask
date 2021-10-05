import os
import base64

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')

# 设备ID(通常是获取手机的imei) 联通判断是否登录多台设备 不能多台设备同时登录 填写常用的设备ID
deviceId = ''

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
    "msg_from": "",  # 发送人qq邮箱
    "password": "",  # 发送人qq邮箱的授权码
    "msg_to": "",  # 收件人邮箱 (发送人和接收人可以相同)
    # pushplus(微信公众号接收消息推送)
    "token": "",  # pushplus消息推送token,
}
