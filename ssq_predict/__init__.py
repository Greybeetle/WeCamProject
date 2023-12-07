#!/usr/bin/env python
# -*- coding: utf-8 -*-
# CREATE TIME: 2023/11/20 14:09
# FILE: __init__.py
# SOFTWARE: PyCharm
# AUTHOR: hosea

"""
ssq预测信息入口
"""
import pandas as pd
from flask import Flask
from flask_bootstrap import Bootstrap
from datetime import datetime
from .config import Config, random_nums
from .generateSsqNums import RandomSsqNums
from utils.setup_logger import setup_logger
from .SSQModel import db, SSQHistory, SSQPredict
from .getSsqData import SsqData
from .sendMessage import MessageSender

logger = setup_logger("init")


def create_app():
    """
    :return:
    """
    app = Flask(__name__)
    Bootstrap(app)

    ssq_data = SsqData()

    def get_history_data():
        current_local_number = SSQHistory.query.order_by(SSQHistory.open_order.desc()).first()
        if current_local_number is None:
            logger.info("当前数据库中历史数据为空，即将从网页上获取最新的历史数据...")
            current_local_number = 1
            current_remote_number = ssq_data.get_current_remote_number()  # 获取远端最新的期号
            history_data = ssq_data.get_history_data(current_local_number, current_remote_number)  # 获取远端最新的历史数据，同时保存到数据库中
            logger.info("成功获取全量数据，将数据保存到数据库中...")
            with app.app_context():
                history_data_dict = [(history_data.iloc[__index, :]).to_dict() for __index in range(0, history_data.shape[0])]
                db.session.bulk_insert_mappings(SSQHistory, history_data_dict)
                db.session.commit()
            current_local_number = current_remote_number
            logger.info("已保存最新的历史数据到数据库中...")
        else:
            current_local_number = current_local_number.open_order
            logger.info("从数据库中读取当前库中的所有数据，开始对比本地最新期号和远端最新期号...")
            temp = []
            for his in SSQHistory.query.all():
                temp.append([his.open_order, his.open_date, his.red_num_1, his.red_num_2, his.red_num_3, his.red_num_4, his.red_num_5, his.red_num_6, his.blue_num])
            history_data = pd.DataFrame(temp, columns=['期号', '开奖日期', '红球_1', '红球_2', '红球_3', '红球_4', '红球_5', '红球_6', '蓝球'])
            current_remote_number = ssq_data.get_current_remote_number()  # 获取远端最新的期号
            if current_local_number == current_remote_number:
                logger.info("当前本地数据与官网最新数据期号一致，使用本地数据...")
            else:
                logger.info("当前本地数据与官网最新数据期号不一致，从远端获取最新的数据...")
                _history_data = ssq_data.get_history_data(current_local_number+1, current_remote_number)  # 获取远端最新的历史数据，同时保存到数据库中
                logger.info("将最新的数据追加写入数据库中...")
                with app.app_context():
                    _history_data_dict = [(_history_data.iloc[__index, :]).to_dict() for __index in range(0, _history_data.shape[0])]
                    db.session.bulk_insert_mappings(SSQHistory, _history_data_dict)
                    db.session.commit()
                current_local_number = current_remote_number
                history_data = pd.concat([history_data, _history_data], axis=1)

        return history_data, current_local_number

    @app.route("/random_ssq")
    def random_ssq():
        history_data, current_number = get_history_data()

        # 生成待选的数据组
        rsn = RandomSsqNums(random_groups=10, current_number=current_number, ssq_history_data=history_data)
        random_ssq_nums = rsn.get_random_ssq_nums()

        # 首先删除掉以前生成的随机数组
        db.session.query(SSQPredict).delete()
        db.session.commit()
        # 将生成的数据组写入到数据库中
        with app.app_context():
            random_ssq_nums_dict = [(random_ssq_nums.iloc[__index, :]).to_dict() for __index in range(0, random_ssq_nums.shape[0])]
            db.session.bulk_insert_mappings(SSQPredict, random_ssq_nums_dict)
            db.session.commit()
        logger.info("已将随机生成的数据组写入到数据库中...")
        return "200"

    @app.route("/robot")
    def index():
        content = get_message_content()
        print(content)
        message_sender = MessageSender()
        flag, __res_msg = message_sender.send_message(message_type='text', message=content)
        if flag == 0:
            return 'done'
        else:
            return 'err'

    def get_message_content():
        predict_data_sample = pd.DataFrame()
        try:
            current_local_number = SSQHistory.query.order_by(SSQHistory.open_order.desc()).first().open_order  # 从历史数据库中获取最新的期号
        except AttributeError as e:
            random_ssq()
            current_local_number = SSQHistory.query.order_by(
                SSQHistory.open_order.desc()).first().open_order  # 从历史数据库中获取最新的期号
        random_ssq_list = SSQPredict.query.filter(SSQPredict.open_order == current_local_number+1, ).all()

        if len(random_ssq_list) == 0:
            logger.warning("当前数据库中没有预测数据，开始随机生成数据...")
            random_ssq()
            index()
        else:
            __temp = []
            for rr in random_ssq_list:
                __temp.append([rr.id, rr.open_order, rr.red_num_1, rr.red_num_2, rr.red_num_3, rr.red_num_4, rr.red_num_5,
                               rr.red_num_6, rr.blue_num, rr.red_avg, rr.red_big_small, rr.red_mostly_num, rr.red_jishu_count,
                               rr.red_zhishu_count, rr.red_lianhao_count, rr.red_small_mid_big, rr.blue_mostly_num, rr.blue_yilou_count])
            predict_data = pd.DataFrame(__temp,
                                        columns=['编号', '预测期号', '红球_1', '红球_2', '红球_3', '红球_4', '红球_5',
                                                 '红球_6', '蓝球', '红球均值', '红球大小', '红球大概率数字命中个数', '奇数个数',
                                                 '质数个数', '连号个数', '小中大区比', '蓝球是否命中大概率数字', '蓝球是否遗漏超过10次'])

            predict_data_del = predict_data[(predict_data['红球均值'] >= '11') & (predict_data['红球均值'] <= '23')]
            predict_data_del = predict_data_del[(predict_data_del['红球大小'] == '小小大大大大') | (predict_data_del['红球大小'] == '小小小大大大') | (predict_data_del['红球大小'] == '小小小小大大')]
            predict_data_del = predict_data_del[predict_data_del['红球大概率数字命中个数'] >= 3]
            predict_data_del = predict_data_del[(predict_data_del['奇数个数'] >= 2) & (predict_data_del['奇数个数'] <= 5)]
            predict_data_del = predict_data_del[(predict_data_del['质数个数'] != 0) & (predict_data_del['质数个数'] != 5) & (predict_data_del['质数个数'] != 6)]
            predict_data_del = predict_data_del[predict_data_del['连号个数'] <= 2]
            predict_data_del = predict_data_del[(predict_data_del['小中大区比'].str.startswith("0") == False) & (predict_data_del['小中大区比'].str.endswith("0") == False)]
            predict_data_del = predict_data_del[predict_data_del['蓝球是否命中大概率数字'] == 'True']
            predict_data_del = predict_data_del[predict_data_del['蓝球是否遗漏超过10次'] == 'True']

            while True:
                predict_data_sample = predict_data_del.sample(n=random_nums)
                if predict_data_sample['蓝球'].max() - predict_data_sample['蓝球'].min() > random_nums - 2:
                    break

        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        content = '{}\n\n{}期双色球预测结果如下，共{}组\n\n'.format(date, current_local_number+1, random_nums)

        predict_str_list = []

        predict_data_sample_select = predict_data_sample[['红球_1', '红球_2', '红球_3', '红球_4', '红球_5', '红球_6', '蓝球']]

        for p_l in predict_data_sample_select.values:
            pl2str = [str(i) for i in p_l]
            predict_str_list.append(' '.join(pl2str))

        content += '\n'.join(predict_str_list)

        return content

    return app
