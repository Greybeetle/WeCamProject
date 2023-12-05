#!/usr/bin/env python
# -*- coding: utf-8 -*-
# CREATE TIME: 2023/11/5 14:29
# FILE: sendMessage.py
# SOFTWARE: PyCharm
# AUTHOR: hosea

"""
向企业微信定时发送任务的类
"""
import requests, json
from .config import API, appConfig
from utils.setup_logger import setup_logger
logger = setup_logger("sendMessage")


class MessageSender(object):
    def __init__(self, touser='@all', toparty='@all', totag='@all'):
        self.__touser = touser
        self.__toparty = toparty
        self.__totag = totag
        self.__CORPID = appConfig['CORPID']
        self.__AGENGID = appConfig['AGENTID']
        self.__CORPSERET = appConfig['CORPSECRET']

    def __get_access_token(self):
        logger.info("开始验证access token...")
        url = API['ACCESSTOKENAPI'].format(self.__CORPID, self.__CORPSERET)
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        res = response.json()
        if res['errcode'] == 0:
            return res['errcode'], res['access_token']
        else:
            return res['errcode'], res['errmsg']

    def __generate_message_content(self, message, message_type='text'):
        if message_type == 'text':
            message = {
                "touser": self.__touser,
                "toparty": self.__toparty,
                "totag": self.__totag,
                "msgtype": message_type,
                "agentid": appConfig['AGENTID'],
                "text": {
                    "content": message,
                },
                "safe": 0,
                "enable_id_trans": 0,
                "enable_duplicate_check": 0,
                "duplicate_check_interval": 1800
            }
            return json.dumps(message)

    def send_message(self, message_type='text', message=None):
        __res_code, __res_msg = self.__get_access_token()
        if __res_code == 0:
            logger.info("用户access token验证通过...")
            url = API['SENTMESSAGEAPI'].format(__res_msg)
            headers = {'Content-Type': 'text/plain'}
            payload = self.__generate_message_content(message, message_type)
            response = requests.request("POST", url, headers=headers, data=payload)
            res = response.json()
            if res['errcode'] == 0:
                logger.info("发送信息成功，请在企业微信中查收...")
                return res['errcode'], 'send message success！！！'
            else:
                logger.warning("发送信息失败，请查看相关配置...")
                return res['errcode'], 'send message failed, ' + res['errmsg']
        else:
            logger.warning("用户access token验证不通过，请验证相关信息...")
            return 'ERR: get access token failed, ' + __res_msg

