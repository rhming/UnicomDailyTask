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
### 云函数基本使用
+ 执行环境选择python3.6 上传[UnicomDailyTask.zip](https://github.com/rhming/UnicomDailyTask/releases/download/1.0/UnicomDailyTask.zip)到云函数
### 云函数配置
+ 触发配置
> ![image](https://user-images.githubusercontent.com/49028484/132980589-59cd80dd-be5e-4535-92b0-38b4c35b2ca5.png)
+ 环境配置
> ![image](https://user-images.githubusercontent.com/49028484/132981224-2b93c0b2-4be7-4745-a440-d58c61f96598.png)


