#!/usr/bin/env python
# -*- coding: utf-8 -*-
# CREATE TIME: 2023/11/20 17:18
# FILE: add_extra_info.py
# SOFTWARE: PyCharm
# AUTHOR: hosea

"""

"""
import pandas as pd


# 判断red_num大小，16小，17大，排除第一个red_num是大的，最后一个red_num是小的，优先选择“小小大大大大”、“小小小大大大”、“小小小小大大”三种
def check_daxiao(df):
    __res = ''
    __res += '大' if df['red_num_1'] >= 17 else '小'
    __res += '大' if df['red_num_2'] >= 17 else '小'
    __res += '大' if df['red_num_3'] >= 17 else '小'
    __res += '大' if df['red_num_4'] >= 17 else '小'
    __res += '大' if df['red_num_5'] >= 17 else '小'
    __res += '大' if df['red_num_6'] >= 17 else '小'
    return __res


# 根据所有数字之前出现的频次筛选最可能出现的n个数字，随机号码中有三个及以上的数字出现在n个数字中即算作符合条件
def check_pinci(df, maybe_red_num):
    __count = 0
    __count += 1 if df['red_num_1'] in maybe_red_num else 0
    __count += 1 if df['red_num_2'] in maybe_red_num else 0
    __count += 1 if df['red_num_3'] in maybe_red_num else 0
    __count += 1 if df['red_num_4'] in maybe_red_num else 0
    __count += 1 if df['red_num_5'] in maybe_red_num else 0
    __count += 1 if df['red_num_6'] in maybe_red_num else 0
    return __count


# 判断奇偶数情况，剔除奇偶比为0：6或者6：0的组合
def check_jiou(df):
    __jishu_count = 0
    __jishu_count += 0 if df['red_num_1'] % 2 == 0 else 1
    __jishu_count += 0 if df['red_num_2'] % 2 == 0 else 1
    __jishu_count += 0 if df['red_num_3'] % 2 == 0 else 1
    __jishu_count += 0 if df['red_num_4'] % 2 == 0 else 1
    __jishu_count += 0 if df['red_num_5'] % 2 == 0 else 1
    __jishu_count += 0 if df['red_num_6'] % 2 == 0 else 1
    return __jishu_count


# 5. 判断质合数情况，剔除质合比为0：6、5：1及6：0的组合
def check_zhihe(df):
    __zhishu_list = [1, 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    __zhishu_count = 0
    __zhishu_count += 1 if df['red_num_1'] in __zhishu_list else 0
    __zhishu_count += 1 if df['red_num_2'] in __zhishu_list else 0
    __zhishu_count += 1 if df['red_num_3'] in __zhishu_list else 0
    __zhishu_count += 1 if df['red_num_4'] in __zhishu_list else 0
    __zhishu_count += 1 if df['red_num_5'] in __zhishu_list else 0
    __zhishu_count += 1 if df['red_num_6'] in __zhishu_list else 0
    return __zhishu_count


# 6. 连号情况筛选，连号组数不能超过2组，每组连号个数不能超过2个
def check_lianhao(df):
    __lianhao_nums = 0
    __list = df[['red_num_1', 'red_num_2', 'red_num_3', 'red_num_4', 'red_num_5', 'red_num_6']].to_list()

    for i in range(0, 5):
        if __list[i + 1] - __list[i] == 1:
            __lianhao_nums += 1

    return __lianhao_nums


# 7. red_num三分区走势
def check_sanfenqu(df):
    __max_counts = 0
    __mid_counts = 0
    __min_counts = 0
    __list = df[['red_num_1', 'red_num_2', 'red_num_3', 'red_num_4', 'red_num_5', 'red_num_6']].to_list()

    for ll in __list:
        if ll <= 11:
            __min_counts += 1
        elif ll >= 23:
            __max_counts += 1
        else:
            __mid_counts += 1
    return str(__min_counts) + str(__mid_counts) + str(__max_counts)


# 8. 筛选篮球1,根据所有数字之前出现的频次筛选最可能出现的n个数字进行匹配
def check_blue_pinci(df, maybe_blue_num):
    # 计算当前历史数据每个数的出现次数，出现次数最低的5个数下次最有可能出现
    if df['blue_num'] in maybe_blue_num:
        return 'True'
    else:
        return 'False'


# 9. 筛选篮球2
def check_blue_yilou(df, __dd):
    # 计算当前历史数据每个数的遗漏次数，遗漏次数最高的5个数字最有可能出现
    __res = {}
    __dd = __dd.reset_index()
    for i in range(1, 17):
        __temp = __dd[__dd['蓝球'] == i].head(1)['index'].to_list()
        __res[i] = __temp[0] + 1

    __temp_blue_df = pd.DataFrame(__res, index=["当前遗漏次数"]).T.reset_index()
    __temp_blue_df.columns = ['号码', '当前遗漏次数']
    __temp_blue_df.sort_values(by='当前遗漏次数', ascending=False, inplace=True)
    __temp_blue_list = __temp_blue_df.head(10)['号码'].to_list()

    if df['blue_num'] in __temp_blue_list:
        return 'True'
    else:
        return 'False'

