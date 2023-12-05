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

scheduler = APScheduler()

app = create_app()

app.config.from_object(config.Config)

# 初始化数据库
db.init_app(app)
app.app_context().push()
db.create_all()  # 创建所有的表

scheduler.init_app(app)
scheduler.start()


# @scheduler.task('cron', hour='16', second='00')
def random_ssq_scheduler():
    url = "http://127.0.0.1:{}/random_ssq".format(config.run_config['PORT'])

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.text == '200':
        print("done")
    else:
        print("false")


if __name__ == '__main__':
    app.run(port=config.run_config['PORT'])
