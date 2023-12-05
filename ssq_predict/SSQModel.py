#!/usr/bin/env python
# -*- coding: utf-8 -*-
# CREATE TIME: 2023/11/20 22:31
# FILE: SSQModel.py
# SOFTWARE: PyCharm
# AUTHOR: hosea

"""
设置Model
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class SSQHistory(db.Model):
    __tablename__ = 'tb_ssq_history'
    open_order = db.Column("期数", db.Integer, primary_key=True)
    open_date = db.Column("开奖日期", db.String(20))
    red_num_1 = db.Column('红球_1', db.Integer)
    red_num_2 = db.Column('红球_2', db.Integer)
    red_num_3 = db.Column('红球_3', db.Integer)
    red_num_4 = db.Column('红球_4', db.Integer)
    red_num_5 = db.Column('红球_5', db.Integer)
    red_num_6 = db.Column('红球_6', db.Integer)
    blue_num = db.Column('蓝球', db.Integer)


class SSQPredict(db.Model):
    __tablename__ = 'tb_ssq_predict'

    #
    id = db.Column('id', db.Integer, primary_key=True)
    open_order = db.Column(u"预测期数", db.Integer)
    red_num_1 = db.Column(u'红球_1', db.Integer)
    red_num_2 = db.Column(u'红球_2', db.Integer)
    red_num_3 = db.Column(u'红球_3', db.Integer)
    red_num_4 = db.Column(u'红球_4', db.Integer)
    red_num_5 = db.Column(u'红球_5', db.Integer)
    red_num_6 = db.Column(u'红球_6', db.Integer)
    blue_num = db.Column(u'蓝球', db.Integer)
    red_avg = db.Column(u'红球均值', db.String(10))
    red_big_small = db.Column(u'红球大小', db.String(10))
    red_mostly_num = db.Column(u'红球大概率数字命中个数', db.Integer)
    red_jishu_count = db.Column(u'奇数个数', db.Integer)
    red_zhishu_count = db.Column(u'质数个数', db.Integer)
    red_lianhao_count = db.Column(u'连号个数', db.Integer)
    red_small_mid_big = db.Column(u'小中大区比', db.String(10))
    blue_mostly_num = db.Column(u'蓝球是否命中大概率数字', db.String(5))
    blue_yilou_count = db.Column(u'蓝球是否遗漏超过10次', db.String(5))
