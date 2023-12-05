#!/usr/bin/env python
# -*- coding: utf-8 -*-
# CREATE TIME: 2023/11/20 14:08
# FILE: config.py
# SOFTWARE: PyCharm
# AUTHOR: hosea

"""

"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    flask_ENV = 'development'
    DEBUG = False
    SECRET_KEY = '_5#y2L"F4Q8zxec]/'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1234qwer@localhost:3306/db_HomeSpace'  # 本地测试
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:ghx19940727,.@124.221.249.48:3306/db_HomeSpace"  # 本地测试
    UPLOAD_FOLDER = os.path.join(basedir, 'upload\\')


# 双色球数据相关参数
SSQ = {
    'data_path': 'data/data.csv',
    'base_url': 'https://datachart.500.com/ssq/history/'
}

run_config = {
    'PORT': '5000',
    'HOST': '0.0.0.0'
}

random_nums = 2

# 企业微信参数配置
appConfig = {
    'CORPID': 'ww8a9efe30dded2cb9',  # 企业id

    'AGENTID': '1000006',  # 应用id
    'CORPSECRET': 'hUMhVjdd-lGVVBmlY8gTX2U7tUd9gsnEMqgGAp5Ul5M',  # 应用secret

    'sToken': 'fDKZEIkJpuG6',  # API接收消息服务器Token
    'sEncodingAESKey': '1uHQKQYv6ND6R7yfRj9gKIE9NDm95YhvoQuhNDaGndt'  # API接收消息服务器EncodingAESKey
}

# 发送消息涉及的API
API = {
    "ACCESSTOKENAPI": 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}',
    "SENTMESSAGEAPI": 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}'
}
