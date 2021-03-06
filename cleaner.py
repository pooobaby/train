#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright By Eric in 2020

import itertools
from itertools import groupby
import pandas as pd
from pymongo import MongoClient


# noinspection PyPep8Naming
class Cleaning(object):
    def __init__(self):
        self.client = MongoClient('localhost', port=27017)
        self.db = self.client.train
        self.train = self.db.Train
        self.station = self.db.StationGeo

        self.train_df = pd.DataFrame(self.train.find({}, {'_id': 0}))
        self.train_df = self.train_df.drop_duplicates(subset='No', keep='first', inplace=False)

        self.station_df = pd.DataFrame(self.station.find({}, {'_id': 0}))
        self.station_df = self.station_df.drop_duplicates(subset='name', keep='first', inplace=False)

        self.type_dict = {'高速动车组': 'G', '普通动车组': 'D', '城际动车组': 'C', '快速': 'K',
                          '普快': '9', '直达特快': 'Z', '特快': 'T', '其他': 'O'}

    def printResult(self):
        """
        -- 打印输出模块
        :return:
        """
        trains = self.train_df.shape[0]
        start_stations = self.train_df.loc[:, 'start_s'].value_counts().shape[0]
        end_stations = self.train_df.loc[:, 'end_s'].value_counts().shape[0]
        kms = sum(list(map(int, self.train_df.km.tolist())))
        hours = sum(self.changePeriod().time.tolist()) // 60

        count_by_city = self.countByCity()[:20]
        print('\n-- 全国火车站数量最多的前20个城市如下：')
        for n in range(len(count_by_city)):
            print('{0:>3}. {1:{3}<10}: {2:{3}<5}'
                  .format(n+1, count_by_city[n][0], count_by_city[n][1], chr(12288)))

        count_by_province = self.countByProvince()
        print('\n-- 全国各省、市、自治区火车站数量分布如下：')
        for n in range(len(count_by_province)):
            print('{0:>3}. {1:{3}<10}: {2:{3}<5}'
                  .format(n+1, count_by_province[n][0], count_by_province[n][1], chr(12288)))

        count_by_type = self.countByType()
        print('\n-- 数据库中共有%d次列车。' % trains)
        for n in count_by_type:
            print('{0:>3}. {1:{3}<6}: {2:{3}<5}'.format(self.type_dict[n[0]], n[0], n[1], chr(12288)))

        count_by_start_Station = self.countByStartStation()
        print('\n-- 共有%d个车站是始发站，始发列车最多的前20个车站:' % start_stations)
        for n in range(20):
            print('{0:{4}>3}. {1:{3}<6}: {2:{4}<5}'
                  .format(n+1, count_by_start_Station[n][0], count_by_start_Station[n][1], chr(12288), ' '))

        count_by_end_Station = self.countByEndStation()
        print('\n-- 共有%d个车站是终点站，终到列车最多的前20个车站:' % end_stations)
        for n in range(20):
            print('{0:{4}>3}. {1:{3}<6}: {2:{4}<5}'
                  .format(n+1, count_by_end_Station[n][0], count_by_end_Station[n][1], chr(12288), ' '))

        count_by_station = self.countByStation()
        print('\n-- 全国共有%d个车站，经过列车最多的前20个车站:' % len(count_by_station))
        for n in range(1, 21):
            print('{0:{4}>3}. {1:{3}<6}: {2:{4}<5}'
                  .format(n, count_by_station[n-1][0], count_by_station[n-1][1], chr(12288), ' '))

        count_by_distance = self.countByDistance()
        print('\n-- 全国每天运行的旅客列车总里程{:,}公里，各里程区间运行的列车数量如下：'.format(kms))
        for k in count_by_distance:
            print('{0:{2}>12}Km : {1:{2}<6}'.format(k[0], k[1], ' '))

        count_by_top_distance = self.countByTopDistance()
        max_20_d = count_by_top_distance.iloc[:20, ]  # 切片取得前20行
        min_20_d = count_by_top_distance.iloc[-20:, ]  # 切片取得后20行
        print('\n-- 全国运行里程最长的列车是{}次，运行里程最长的前20次列车信息如下：'.format(max_20_d.iat[0, 0]))
        print('{9:{1}>3}  {2:{1}^12}{3:{0}^7} {4:{0}^8} {5:{0}^8} {6:{1}^4} {7:{1}^6} {8:{1}^6}'
              .format(chr(12288), ' ', '车次', '类型', '始发站', '终点站', '里程', '时间', '站点', ' '))
        for n in range(0, 20):
            print('{9:{1}>3}. {2:{1}^12} {3:{0}^7} {4:{0}^8} {5:{0}^8} {6:{1}^6} {7:{1}^8} {8:{1}^6}'
                  .format(chr(12288), ' ', max_20_d.iat[n, 0], max_20_d.iat[n, 1], max_20_d.iat[n, 2],
                          max_20_d.iat[n, 3], max_20_d.iat[n, 4], max_20_d.iat[n, 5], max_20_d.iat[n, 6],
                          n + 1))

        print('\n-- 全国运行里程最短的列车是{}次，运行里程最短的后20次列车信息如下：'.format(min_20_d.iat[-1, 0]))
        print('{9:{1}>3}  {2:{1}^12}{3:{0}^7} {4:{0}^8} {5:{0}^8} {6:{1}^4} {7:{1}^6} {8:{1}^6}'
              .format(chr(12288), ' ', '车次', '类型', '始发站', '终点站', '里程', '时间', '站点', ' '))
        for n in range(1, 21):
            print('{9:{1}>3}. {2:{1}^12} {3:{0}^7} {4:{0}^8} {5:{0}^8} {6:{1}^6} {7:{1}^8} {8:{1}^6}'
                  .format(chr(12288), ' ', min_20_d.iat[-n, 0], min_20_d.iat[-n, 1], min_20_d.iat[-n, 2],
                          min_20_d.iat[-n, 3], min_20_d.iat[-n, 4],
                          min_20_d.iat[-n, 5], min_20_d.iat[-n, 6], n))

        count_by_type_distance = self.countByTypeDistance()
        for t in range(len(count_by_type_distance)):
            print('\n-- 全国运行里程最长的{}列车是{}次，运行里程最长的前10次列车信息如下：'
                  .format(count_by_type_distance[t].iat[0, 1], count_by_type_distance[t].iat[0, 0]))
            print('{9:{1}>3}  {2:{1}^12}{3:{0}^7} {4:{0}^8} {5:{0}^8} {6:{1}^4} {7:{1}^6} {8:{1}^6}'
                  .format(chr(12288), ' ', '车次', '类型', '始发站', '终点站', '里程', '时间', '站点', ' '))
            for n in range(count_by_type_distance[t].shape[0]):
                print('{9:{1}>3}. {2:{1}^12} {3:{0}^7} {4:{0}^8} {5:{0}^8} {6:{1}^6} {7:{1}^8} {8:{1}^6}'
                      .format(chr(12288), ' ', count_by_type_distance[t].iat[n, 0], count_by_type_distance[t].iat[n, 1],
                              count_by_type_distance[t].iat[n, 2], count_by_type_distance[t].iat[n, 3],
                              count_by_type_distance[t].iat[n, 4], count_by_type_distance[t].iat[n, 5],
                              count_by_type_distance[t].iat[n, 6], n + 1))

        count_by_period = self.countByPeriod()
        print('\n-- 全国每天运行的旅客列车总时长为{:,}小时，各时长区间运行的列车数量如下：'.format(hours))
        for p in count_by_period:
            print('{0:{2}>12}h : {1:{2}<6}'.format(p[0], p[1], ' '))

        count_by_top_period = self.countByTopPeriod()
        max_20_p = count_by_top_period.iloc[:20, ]      # 切片取得前20行
        min_20_p = count_by_top_period.iloc[-20:, ]     # 切片取得后20行
        print('\n-- 全国运行时间最长的列车是{}次，运行时间最长的前20次列车信息如下：'.format(max_20_p.iat[0, 0]))
        print('{9:{1}>3}  {2:{1}^12}{3:{0}^7} {4:{0}^8} {5:{0}^8} {6:{1}^4} {7:{1}^6} {8:{1}^6}'
              .format(chr(12288), ' ', '车次', '类型', '始发站', '终点站', '里程', '时间', '站点', ' '))
        for n in range(0, 20):
            print('{9:{1}>3}. {2:{1}^12} {3:{0}^7} {4:{0}^8} {5:{0}^8} {6:{1}^6} {7:{1}^8} {8:{1}^6}'
                  .format(chr(12288), ' ', max_20_p.iat[n, 0], max_20_p.iat[n, 1], max_20_p.iat[n, 2],
                          max_20_p.iat[n, 3], max_20_p.iat[n, 4], max_20_p.iat[n, 5], max_20_p.iat[n, 7],
                          n + 1))

        print('\n-- 全国运行时间最短的列车是{}次，运行时间最短的后20次列车信息如下：'.format(min_20_p.iat[-1, 0]))
        print('{9:{1}>3}  {2:{1}^12}{3:{0}^7} {4:{0}^8} {5:{0}^8} {6:{1}^4} {7:{1}^6} {8:{1}^6}'
              .format(chr(12288), ' ', '车次', '类型', '始发站', '终点站', '里程', '时间', '站点', ' '))
        for n in range(1, 21):
            print('{9:{1}>3}. {2:{1}^12} {3:{0}^7} {4:{0}^8} {5:{0}^8} {6:{1}^6} {7:{1}^8} {8:{1}^6}'
                  .format(chr(12288), ' ', min_20_p.iat[-n, 0], min_20_p.iat[-n, 1], min_20_p.iat[-n, 2],
                          min_20_p.iat[-n, 3], min_20_p.iat[-n, 4],
                          min_20_p.iat[-n, 5], min_20_p.iat[-n, 7], n))

        count_by_speed = self.countBySpeed()
        print('\n-- 各种类型的列车中，%s的速度最快，按速度对类型排序结果如下:' % count_by_speed[0][0])
        for n, value in enumerate(count_by_speed):
            print('{0:{4}>3}. {1:{3}<6}: {2:{4}<5}Km/h'
                  .format(n + 1, count_by_speed[n][0], int(count_by_speed[n][1]), chr(12288), ' '))

        return

    def countByCity(self):
        """
        -- 按城市统计车站数量
        :return:list: [(城市名称, 值)]
        """
        count_list = []
        cities = self.station_df.loc[:, 'city'].value_counts()
        for n, value in cities.items():
            if len(n) == 0:
                continue
            count_list.append((n, value))
        return count_list

    def countByProvince(self):
        """
        -- 按省份统计车站数量
        :return:list: [(省份名称, 值)]
        """
        count_list = []
        provinces = self.station_df.loc[:, 'province'].value_counts()
        for n, value in provinces.items():
            n = n.replace('省', '').replace('市', '').replace('自治区', '').replace('维吾尔', '').replace('回族', '')\
                .replace('壮族', '').replace('特别行政区', '')
            count_list.append((n, value))
        return count_list

    def countByType(self):
        """
        -- 按列车类型统计
        series.items()用于遍历series对象，同时列出索引和值。
        '{0} {1:{3}<6}: {2:{3}<5}'为格式化输出，中文字空格编码为chr(12288)，用来占位
        :return:list: [(类型名称, 值)]
        """
        count_list = []
        types = self.train_df.loc[:, 'type'].value_counts()
        for n, value in types.items():
            count_list.append((n, value))
        return count_list

    def countByStartStation(self):
        """
        -- 按始发站统计，并格式化输出
        enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列,同时列出数据和数据下标
        :return: list: [(车站名称, 值)]
        """
        start_s = self.train_df.loc[:, 'start_s'].value_counts()
        start_s_list = []
        for n, value in enumerate(start_s):
            start_s_list.append((start_s.index[n], value))
        return start_s_list

    def countByEndStation(self):
        """
        -- 按终点站统计，并格式化输出
        enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列,同时列出数据和数据下标
        :return: list: [(车站名称, 值)]
        """
        end_s = self.train_df.loc[:, 'end_s'].value_counts()
        end_s_list = []
        for n, value in enumerate(end_s):
            end_s_list.append((end_s.index[n], value))
        return end_s_list

    def countByStation(self):
        """
        -- 按列车经过的所有车站统计，并格式化输出
        尝试了多种方法，下面应该是最优化的算法，能不用遍历就不用
        :return: list: [(车站名称, 值)]
        """
        station = self.train_df.key.tolist()
        s_list = list(itertools.chain(*station))        # 用itertools库展开列表效率更高
        s_df = pd.DataFrame(s_list, columns=['s'])      # 将所有车站的列表转换成df，列名为's'
        s_df_dup = s_df.loc[:, 's'].value_counts().reset_index()   # 列表转成DataFrame后统计重复值、重设索引，
        s_df_turn = s_df_dup.T.values.tolist()       # 使用T来转置数据，也就是行列转换
        station_list = list(zip(s_df_turn[0], s_df_turn[1]))      # zip()可以把两个列表转换为嵌套元组的列表
        return station_list

    def countByDistance(self):
        """
        -- 按列车运行里程统计，生成里程区间，并格式化输出
        涉及到转换列表元素类型，groupby()函数的使用
        :return: list: [(里程区间, 值)]
        """
        km = self.train_df.km.tolist()
        km = list(map(int, km))     # 将列表中的元素转换为整数型
        km_list = []
        km_dict = {}
        for k, g in groupby(sorted(km), key=lambda x: x // 100):    # 使用groupby()函数将里程按100为区间统计个数
            km_dict['{}'.format(k * 100)] = len(list(g))
        sum_15_20, sum_20_30, sum_30 = 0, 0, 0
        for n in range(len(km_dict)):
            if n < 15:
                km_list.append((('{}-{}'.format(n*100, (n+1)*100-1)), km_dict[str(n*100)]))
            elif 20 > n >= 15:
                sum_15_20 += km_dict[str(n*100)]
            elif 30 > n >= 20:
                sum_20_30 += km_dict[str(n*100)]
            else:
                sum_30 += km_dict[str(n*100)]
        km_list.append(('1500-1999', sum_15_20))
        km_list.append(('2000-2999', sum_20_30))
        km_list.append(('>3000', sum_30))
        return km_list

    def countByTopDistance(self):
        """
        -- 按列车运行里程排序
        涉及将df列中的数值转换类型，根据某一列的值进行处理生成新列，
        :return: df: 按运行里程排序后的df
        """
        km_top = self.sortDistance()        # 调用里程排序函数
        return km_top

    def countByTypeDistance(self):
        """
        -- 按不同类型的列车运行里程排序，，格式化输出前10名
        :return: list[df, df...]: [高速动车组最长里程Top_10, 普通动车组最长里程Top_10...]
        """
        type_d_list = []
        type_d = self.sortDistance()        # 调用里程排序函数
        for t in self.type_dict:
            type_n = type_d[type_d['type'].isin([t])]
            type_n = type_n.sort_values(by='km', ascending=False)
            max_type_n = type_n.iloc[:10]
            type_d_list.append(max_type_n)
        return type_d_list

    def countByPeriod(self):
        """
        -- 按列车运行区间统计，生成运行区间，并格式化输出
        分区间生成数据遍历时，用的方法与countByDistance()的略有不同
        :return: list: [(运行区间, 值)]
        """
        period = self.changePeriod()        # 调用转换运行时间函数
        period_dict = {}
        period_list = []
        periods = period.time.tolist()
        for k, g in groupby(sorted(periods), key=lambda x: x // 120):    # 使用groupby()函数将时间按60为区间统计个数
            period_dict['{}'.format(k)] = len(list(g))
        sum_8_12, sum_12_18, sum_18_24, sum_24_36, sum_36_48, sum_48 = 0, 0, 0, 0, 0, 0
        for n in period_dict:
            n = int(n)
            if n < 4:
                period_list.append((('{}-{}'.format(n*2, (n+1)*2)), period_dict[str(n)]))
            elif 6 > n >= 4:
                sum_8_12 += period_dict[str(n)]
            elif 9 > n >= 6:
                sum_12_18 += period_dict[str(n)]
            elif 12 > n >= 9:
                sum_18_24 += period_dict[str(n)]
            elif 18 > n >= 12:
                sum_24_36 += period_dict[str(n)]
            elif 24 > n >= 18:
                sum_36_48 += period_dict[str(n)]
            else:
                sum_48 += period_dict[str(n)]
        period_list.append(('8-12', sum_8_12))
        period_list.append(('12-18', sum_12_18))
        period_list.append(('18-24', sum_18_24))
        period_list.append(('24-36', sum_24_36))
        period_list.append(('36-48', sum_36_48))
        period_list.append(('>48', sum_48))
        return period_list

    def countByTopPeriod(self):
        """
        -- 按列车运行时间排序
        涉及将df列中的数值转换类型，根据某一列的值进行处理生成新列，
        :return: df: 列车运行时间排序后的df
        """
        period_top = self.changePeriod()        # 调用转换运行时间函数

        period_top = period_top.sort_values(by='time', ascending=False)  # 按time列降序排序
        period_top['key_n'] = period_top.key.apply(lambda x: len(x))  # 取key列中列表的长度，生成新列
        period_top = period_top.drop(columns=['key', 'hour', 'min', 'time'])  # 删除key列
        period_top = period_top.drop_duplicates(subset='km', keep='first')  # 删除重复行
        return period_top

    def countBySpeed(self):
        """
        -- 按运行速度对类型进行排序，并格式化输出
        计算过程中运行总时间包含了到站停车时间，因此不是很精确，待以后处理
        2020-03-03:加入了计算每次列车停车时间，修订计算方式的BUG
        :return: list: [(类型名称, 值)]
        """
        s_list = []
        speed = self.changePeriod()     # 调用转换运行时间函数

        speed['km'] = speed['km'].apply(pd.to_numeric)  # 将min列转换为整数型
        for n in range(speed.shape[0]):         # 用遍历提取infos列中的数据，用以计算停车时间
            info = speed.iat[n, 7]
            stop_time_n = 0
            for city in info:
                if info[city]['st'] == '始发站':
                    continue
                elif info[city]['et'] == '终点站':
                    break
                else:
                    time_out = int(info[city]['et'].split(':')[0])*60 + int(info[city]['et'].split(':')[1])
                    time_in = int(info[city]['st'].split(':')[0])*60 + int(info[city]['st'].split(':')[1])
                    stop_time_n += time_out - time_in
            speed.iat[n, 10] = speed.iat[n, 10] - stop_time_n
        for n in self.type_dict:
            speed_n = speed[speed['type'].isin([n])]
            km_n = speed_n.km.tolist()
            speed_n_s = speed_n.time.tolist()
            n_speed = int(sum(km_n)/sum(speed_n_s)*60)
            s_list.append((n, n_speed))
        speed_list = sorted(s_list, key=lambda s: s[1], reverse=True)
        return speed_list

    def changePeriod(self):
        """
        -- 基础函数，用来根据period列的值进行分解处理，生成time列
        :return: df:包含time列
        """
        change = self.train_df[['code', 'type', 'start_s', 'end_s', 'km', 'period', 'key', 'infos']].copy()
        change['hour'] = change.period.apply(lambda x: x.split(':')[0])  # 分割period列生成hour列
        change['min'] = change.period.apply(lambda x: x.split(':')[1])  # 分割period列生成min列
        change['hour'] = change['hour'].apply(pd.to_numeric)  # 将hour列转换为整数型
        change['min'] = change['min'].apply(pd.to_numeric)  # 将min列转换为整数型
        change['time'] = change[['hour', 'min']].apply(lambda x: x['hour'] * 60 + x['min'], axis=1)
        return change

    def sortDistance(self):
        """
        -- 基础函数，用来根据km列的值进行排序，并将key列中的值生成key_n列
        :return: df:包含key_n列
        """
        distance = self.train_df[['code', 'type', 'start_s', 'end_s', 'km', 'period', 'key']].copy()
        distance['km'] = distance['km'].apply(pd.to_numeric)  # 将km列中的数值转换成整数型
        distance = distance.sort_values(by='km', ascending=False)  # 按km列降序排序
        distance['key_n'] = distance.key.apply(lambda x: len(x))  # 取key列中列表的长度，生成新列
        distance = distance.drop(columns='key')  # 删除key列
        distance = distance.drop_duplicates(subset='km', keep='first')  # 删除重复行
        return distance

    @staticmethod
    def changeXY(data):
        x_data, y_data = [], []
        for n in data:
            x_data.append(n[0])
            y_data.append(n[1])
        result_list = [x_data, y_data]
        return result_list


def main():
    cleaning = Cleaning()
    cleaning.printResult()


if __name__ == '__main__':
    main()
