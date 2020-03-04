#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright By Eric in 2020

import time
from painter import Drawing
from cleaner import Cleaning
from pyecharts.charts import Page


class Train(object):
    def __init__(self):
        self.page = Page(page_title="全国铁路旅客列车数据可视化图表")
        self.drawer = Drawing()
        self.cleaner = Cleaning()

    def exec(self):
        geo_station_data = self.cleaner.countByStation()
        map_province_data = self.cleaner.countByProvince()

        type_data = self.cleaner.countByType()

        start_station_data = self.cleaner.countByStartStation()[:20]
        bar_start_station_data = self.cleaner.changeXY(start_station_data)

        end_station_data = self.cleaner.countByEndStation()[:20]
        bar_end_station_data = self.cleaner.changeXY(end_station_data)

        station_data = self.cleaner.countByStation()[:20]
        bar_station_data = self.cleaner.changeXY(station_data)

        distance_data = self.cleaner.countByDistance()[:20]
        bar_distance_data = self.cleaner.changeXY(distance_data)

        period_data = self.cleaner.countByPeriod()[:20]
        bar_period_data = self.cleaner.changeXY(period_data)

        speed_data = self.cleaner.countBySpeed()[:20]
        bar_speed_data = self.cleaner.changeXY(speed_data)

        self.page.add(self.drawer.geoStation(geo_station_data))
        self.page.add(self.drawer.mapProvince(map_province_data))
        self.page.add(self.drawer.pieType(type_data))
        self.page.add(self.drawer.barStartStation(bar_start_station_data))
        self.page.add(self.drawer.barEndStation(bar_end_station_data))
        self.page.add(self.drawer.barStation(bar_station_data))
        self.page.add(self.drawer.barDistance(bar_distance_data))
        self.page.add(self.drawer.barPeriod(bar_period_data))
        self.page.add(self.drawer.barSpeed(bar_speed_data))

        self.page.render('train.html')
        print('数据地图生成完毕，请打开浏览器查看，多谢。')


def main():
    time_start = time.time()
    print('开始清理数据并生成地图，请稍候......')
    train = Train()
    train.exec()
    time_end = time.time()
    print('程序执行时间：{:.04f}'.format(time_end - time_start))


if __name__ == '__main__':
    main()
