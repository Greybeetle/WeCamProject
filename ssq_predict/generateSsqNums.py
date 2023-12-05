#!/usr/bin/env python
# -*- coding: utf-8 -*-
# CREATE TIME: 2023/11/20 14:55
# FILE: generateSsqNums.py
# SOFTWARE: PyCharm
# AUTHOR: hosea

"""
本脚本主要用于生成双色球预测号码
"""
from collections import Counter
import random

from utils.setup_logger import setup_logger
from .add_extra_info import *
logger = setup_logger("generateSsqNums")


class RandomSsqNums(object):
    def __init__(self, random_groups, current_number, ssq_history_data):
        self.__random_groups = random_groups
        self.__ssq_current_remote_number = current_number
        self.__ssq_history_data = ssq_history_data

    def get_random_ssq_nums(self):
        logger.info("随机获取{}组双色球数据...".format(self.__random_groups*20))
        self.__random_ssq_nums()  # 获取random*20组备选数据
        logger.info("为随机生成的数据增加辅助计算列...")
        self.__add_extra_info()  # 增加额外的判断信息，返回最终结果，dataframe格式
        return self.__random_ssq_df

        # 该方法主要用于随机生成指定组数的双色球号码，处理逻辑是随机生成100*n（用户需要的组数）组随机数据，然后根据相关规则进行删减
    def __random_ssq_nums(self):
        history_red_str_list = self.__ssq_history_data.apply(lambda x: ','.join([str(xx) for xx in x[2:8]]), axis=1)

        res = []
        while len(res) < self.__random_groups * 20:
            red_nums = sorted(random.sample(range(1, 34), 6))
            blue_nums = random.sample(range(1, 17), 1)
            red_str = ','.join([str(x) for x in red_nums])
            if red_str in history_red_str_list:
                continue
            else:
                res.append(red_nums + blue_nums)
        __random_ssq_df = pd.DataFrame(res, columns=['red_num_1', 'red_num_2', 'red_num_3', 'red_num_4', 'red_num_5', 'red_num_6', 'blue_num'])
        __random_ssq_df['open_order'] = self.__ssq_current_remote_number + 1
        self.__random_ssq_df = __random_ssq_df

    # 增加红求均值字段
    def __add_extra_info(self):
        self.__random_ssq_df['red_avg'] = self.__random_ssq_df.apply(lambda x: str(round((x['red_num_1']+x['red_num_2']+x['red_num_3']+x['red_num_4']+x['red_num_5']+x['red_num_6'])/6, 2)), axis=1)
        self.__random_ssq_df['red_big_small'] = self.__random_ssq_df.apply(lambda x: check_daxiao(x), axis=1)
        maybe_red_num = self.__count_red_nums()
        self.__random_ssq_df['red_mostly_num'] = self.__random_ssq_df.apply(lambda x: check_pinci(x, maybe_red_num), axis=1)
        self.__random_ssq_df['red_jishu_count'] = self.__random_ssq_df.apply(lambda x: check_jiou(x), axis=1)
        self.__random_ssq_df['red_zhishu_count'] = self.__random_ssq_df.apply(lambda x: check_zhihe(x), axis=1)
        self.__random_ssq_df['red_lianhao_count'] = self.__random_ssq_df.apply(lambda x: check_lianhao(x), axis=1)
        self.__random_ssq_df['red_small_mid_big'] = self.__random_ssq_df.apply(lambda x: check_sanfenqu(x), axis=1)
        maybe_blue_num = self.__count_blue_nums()
        self.__random_ssq_df['blue_mostly_num'] = self.__random_ssq_df.apply(lambda x: check_blue_pinci(x, maybe_blue_num), axis=1)
        self.__random_ssq_df['blue_yilou_count'] = self.__random_ssq_df.apply(lambda x: check_blue_yilou(x, self.__ssq_history_data), axis=1)

    # 统计历史数据的相关情况，统计历史数据中各个数字出现的次数
    def __count_red_nums(self):
        __temp_df = self.__ssq_history_data.iloc[:, 2:8]
        __temp_list = __temp_df.values.tolist()

        all_num = []
        for ll in __temp_list:
            for l in ll:
                all_num.append(l)
        __temp_dict = dict(Counter(all_num))
        __temp_dict_df = pd.DataFrame(__temp_dict, index=["出现频次"]).T.reset_index()
        __temp_dict_df.columns = ['号码', '出现频次']
        __temp_dict_df.sort_values(by='出现频次', ascending=True, inplace=True)

        # 取出现频次最低的16个数字作为待选数字
        return __temp_dict_df.head(16)['号码'].to_list()

    def __count_blue_nums(self):
        __res = {}
        blue_num_list = self.__ssq_history_data['蓝球'].to_list()

        __temp_blue_dict = dict(Counter(blue_num_list))
        __temp_blue_df = pd.DataFrame(__temp_blue_dict, index=["出现频次"]).T.reset_index()

        __temp_blue_df.columns = ['号码', '出现频次']
        __temp_blue_df.sort_values(by='出现频次', ascending=True, inplace=True)
        # 取出现频次最低的16个数字作为待选数字
        return __temp_blue_df.head(8)['号码'].to_list()

