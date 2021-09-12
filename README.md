# UnicomDailyTask
联通日常任务 腾讯云函数定时执行

+ 需搭建数据存储服务接口 [pythonanywhere仓库](https://github.com/rhming/pythonanywhere)
+ 沃阅读活动
+ 沃学习活动
+ 沃邮箱活动
+ 联通日常任务

### 部分配置文件说明
```
|-- index.py  # 联通账号配置 微信沃邮箱账号配置
`-- utils
    |-- address.json  # 沃阅读自动领取奖品配置(配置收货地址)
    |-- appId.json  # 联通appId配置
    |-- config.py  # 数据存储服务接口配置
```

### 云函数配置
