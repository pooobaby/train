#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright By Eric in 2020
"""
根据12306的火车站原始数据，进行地理编码查询，
将火车站数据保存到mongoDB中，
同时将地理编码无效的火车站信息保存到csv文件中
"""

import json
import requests
import pandas as pd
from tqdm.std import trange
from pymongo import MongoClient


# noinspection PyPep8Naming
class Station(object):
    def __init__(self):
        self.client = MongoClient('localhost', port=27017)
        self.db = self.client.train
        self.collection = self.db.Station

        self.key = '高德地图API的key'  # 高德地图API的key
        self.txt_filename = r'data\station_base.txt'        # 存储车站信息原始数据的文件
        self.csv_filename = r'data\invalid_station.csv'        # 输出的无法查询地理编码车站数据的文件

    def getLocation(self, address):
        url = 'https://restapi.amap.com/v3/geocode/geo?address=' + address + '站&key=' + self.key
        reps = requests.get(url)
        geo_data = json.loads(reps.text)
        if geo_data['count'] == '0':  # 过滤不能生成地理位置坐标的数据，返回值为0
            return 0
        pos = geo_data['geocodes'][0]['location'].split(',')    # 分隔经纬度
        province = geo_data['geocodes'][0]['province']
        city = geo_data['geocodes'][0]['city']
        if len(city) == 0:      # 如果city返回空值，则取下面的district值
            city = geo_data['geocodes'][0]['district']
        return [province, city, pos[0], pos[1]]     # 返回省、市（区）、经纬度

    def toDatabase(self):
        with open(self.txt_filename, 'r', encoding='utf-8') as f:   # 打开原始数据文件
            data = f.read()
        lists = data.split('@')[1:]     # 分隔数据
        invalid = []        # 初始化无效数据列表
        for n in trange(len(lists)):
            n_split = lists[n].split('|')       # 再次分隔每条数据
            location = self.getLocation(n_split[1])     # 调用地理位置生成函数
            if location == 0:       # 如果不能生成地理坐标，则用'火车站'再次查询
                location = self.getLocation(n_split[1]+'火车')
                if location == 0:       # 如果还不能生成地理坐标，将数据加到库中，同时添加到无效列表中
                    invalid_item = {
                        'serial': n_split[5],
                        'telecode': n_split[2],
                        'name': n_split[1],
                        'name_abbr': n_split[0],
                        'name_pinyin': n_split[3],
                        'province': '',
                        'city': '',
                        'lon': '',
                        'lat': ''
                    }
                    self.collection.insert_one(invalid_item)
                    invalid.append([n_split[5], n_split[2], n_split[1], n_split[0], n_split[3]])
                    continue
            item = {
                'serial': n_split[5],
                'telecode': n_split[2],
                'name': n_split[1],
                'name_abbr': n_split[0],
                'name_pinyin': n_split[3],
                'province': location[0],
                'city': location[1],
                'lon': location[2],
                'lat': location[3]
            }
            self.collection.insert_one(item)        # 将数据添加到数据库中
        column = ['serial', 'telecode', 'name', 'name_abbr', 'name_pinyin']     # 定义csv文件的列名
        invalid_df = pd.DataFrame(columns=column, data=invalid)     # 将无效列表转换成DataFrame格式
        invalid_df.to_csv(self.csv_filename)        # 将DataFrame数据输出到csv文件
        print('全部车站信息处理完毕，未查询到地理位置信息的车站共{}个，已保存到{}中：'.format(len(invalid), self.csv_filename))


def main():
    station = Station()
    station.toDatabase()


if __name__ == '__main__':
    main()
