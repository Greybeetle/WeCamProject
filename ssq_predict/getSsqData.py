#!/usr/bin/env python
# -*- coding: utf-8 -*-
# CREATE TIME: 2023/11/20 14:59
# FILE: getSsqData.py
# SOFTWARE: PyCharm
# AUTHOR: hosea


"""
此类用于处理双色球数据下载、获取等
"""
import requests
import pandas as pd
from bs4 import BeautifulSoup
import urllib3
from .config import SSQ
from utils.setup_logger import setup_logger
logger = setup_logger("getssqdata")


class SsqData(object):
    def __init__(self):
        self.__base_url = SSQ['base_url']
        self.__data_path = SSQ['data_path']
        self.__history_data = pd.DataFrame()
        self.__current_remote_number = 0

    def get_current_remote_number(self):
        return self.__spyder_remote_number()

    def get_history_data(self, current_local_number, current_remote_number):
        return self.__spyder_data(current_local_number, current_remote_number)

    def __spyder_remote_number(self):
        """ 获取网站上最新一期期数
        :return: int
        """
        urllib3.disable_warnings()   # 禁用urllib3软件包的证书认证及预警
        r = requests.get(self.__base_url + 'history.shtml', verify=False)
        r.encoding = "gb2312"
        soup = BeautifulSoup(r.text, "html.parser")
        current_remote_num = soup.find("div", class_="wrap_datachart").find("input", id="end")["value"]
        logger.info("当前远端双色球数据最新期号为{}".format(str(current_remote_num)))
        return int(current_remote_num)

    def __spyder_data(self, current_local_number, current_remote_number):
        """ 爬取历史数据
        :return:
        """
        url = '{}{}'.format(self.__base_url, 'newinc/history.php?start={}&end={}'.format(current_local_number, current_remote_number))
        urllib3.disable_warnings()  # 禁用urllib3软件包的证书认证及预警
        r = requests.get(url, verify=False)
        r.encoding = "gb2312"
        soup = BeautifulSoup(r.text, "html.parser")
        trs = soup.find("tbody", attrs={"id": "tdata"}).find_all("tr")
        data = []
        if trs == "":
            logger.warning("抱歉，没有找到数据源！")
        else:
            logger.info("开始下载双色球数据...")
            for tr in trs:
                item = dict()
                item[u"open_order"] = tr.find_all("td")[0].get_text().strip()
                item[u"open_date"] = tr.find_all("td")[-1].get_text().strip()
                for i in range(6):
                    item[u"red_num_{}".format(i+1)] = int(tr.find_all("td")[i+1].get_text().strip())
                item[u"blue_num"] = int(tr.find_all("td")[7].get_text().strip())
                data.append(item)
            self.__history_data = pd.DataFrame(data)
            self.__history_data = self.__history_data.sort_values(by='open_date', ascending=False)
            logger.info("全量双色球数据已下载完成，最新期数为{}期...".format(current_remote_number))
        return self.__history_data

