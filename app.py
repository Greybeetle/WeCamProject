#!/usr/bin/env python
# -*- coding: utf-8 -*-
# CREATE TIME: 2023/11/20 14:07
# FILE: app.py
# SOFTWARE: PyCharm
# AUTHOR: hosea

"""

"""

from ssq_predict import config, create_app, db
from flask_apscheduler import APScheduler
import requests
from utils.setup_logger import setup_logger
logger = setup_logger("app")

scheduler = APScheduler()

app = create_app()

app.config.from_object(config.Config)

# 初始化数据库
db.init_app(app)
app.app_context().push()
db.create_all()  # 创建所有的表

scheduler.init_app(app)
scheduler.start()


@scheduler.task('cron', day_of_week='1, 2, 3, 6', hour='21', minute='32', second='00', timezone='Asia/Shanghai')
def random_ssq_scheduler():
    url = "http://127.0.0.1:{}/random_ssq".format(config.run_config['PORT'])

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.text == '200':
        logger.info("自动生成随机数组成功...")
    else:
        logger.error("自动生成随机数组失败...")


@scheduler.task('cron', day_of_week='1, 2, 3, 6', hour='21', minute='32', second='30', timezone='Asia/Shanghai')
def random_ssq_scheduler():
    url = "http://127.0.0.1:{}".format(config.run_config['PORT'])

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.text == 'done':
        logger.info("自动发送消息成功...")
    else:
        logger.error("自动发送消息失败...")


if __name__ == '__main__':
    app.run(host=config.run_config['HOST'], port=config.run_config['PORT'])
