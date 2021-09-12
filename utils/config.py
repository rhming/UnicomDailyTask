import os
import base64

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')

# 数据存储接口 (需搭建存储接口)
data_storage_server_url = ''  # https://utf8.pythonanywhere.com/

# 数据存储接口授权配置
username = ''  # 账户
password = ''  # 密码
Authorization = 'Basic ' + base64.b64encode(
    ':'.join([username, password]).encode('utf8')
).decode('utf8')
