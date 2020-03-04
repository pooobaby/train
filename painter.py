#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright By Eric in 2020

from pyecharts import options as opts
from pyecharts.charts import Geo, Map, Pie, Bar
from pyecharts.globals import ThemeType     # 主题


# noinspection PyPep8Naming
class Drawing(object):
    def __init__(self):
        self.file_json = r'data\station_geo.json'
        self.data_source = '[数据来源：12306.cn]'

    def geoStation(self, data)-> Geo:
        """
        -- 全国火车站及开行列车数量分布图
        设置主题：theme=ThemeType.DARK，背景颜色：bg_color="#e0f0e9"，设置高亮状态下的样式
        :param data:list:[(车站名称，值)]
        :return: Geo
        """
        station_map = (
            Geo(init_opts=opts.InitOpts(width='1000px', height='500px', theme=ThemeType.DARK))
            .add_schema(maptype="china", zoom=1.2,
                        itemstyle_opts=opts.ItemStyleOpts(color="#323c48", border_color="#111"),
                        emphasis_itemstyle_opts=opts.ItemStyleOpts(color="#323c48"),        # 高亮状态下的多边形样式(省份)
                        emphasis_label_opts=opts.LabelOpts(is_show=False)       # 高亮状态下的标签样式(省份名称)
                        )
            .add_coordinate_json(self.file_json)      # 从json文件导入坐标值
            .add('', data[:2990], symbol_size=2, color='#057748')
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False),
                             markarea_opts=opts.MarkAreaOpts(is_silent=False))       # 关闭各省名称显示
            .set_global_opts(
                visualmap_opts=opts.VisualMapOpts(type_='color', min_=0, max_=100),
                title_opts=opts.TitleOpts(title='全国火车站及开行列车数量分布图',
                                          title_textstyle_opts=opts.TextStyleOpts(font_size=20),  # 设置标题大小
                                          subtitle='全国3500+个车站，开行列车最多的前三个车站是：{}，{}，{}...  {}'
                                          .format(data[0][0], data[1][0], data[2][0], self.data_source))
            )
        )
        return station_map

    def mapProvince(self, data)-> Map:
        """
        -- 全国各省火车站数量
        :param data:list:[(省份名称，值)]
        :return: Map
        """
        province_map = (
            Map(init_opts=opts.InitOpts(width='1000px', height='500px', theme=ThemeType.DARK))
            .add('火车站数量', data, "china", zoom=1.2)
            .set_series_opts(
                label_opts=opts.LabelOpts(is_show=False),       # 关闭各省名称显示
                itemstyle_opts=opts.ItemStyleOpts(color='rgba(255, 255, 255, 0)'))      # 去掉省会的点
            .set_global_opts(
                visualmap_opts=opts.VisualMapOpts(type_='color', min_=0, max_=250),      # 设置最大，最小值
                legend_opts=opts.LegendOpts(is_show=False),     # 不显示图例
                title_opts=opts.TitleOpts(title='全国各省火车站数量分布',
                                          title_textstyle_opts=opts.TextStyleOpts(font_size=20),    # 设置标题大小
                                          subtitle='全国3500+个车站，数量最多的前三个省是：{}，{}，{}...  {}'
                                          .format(data[0][0], data[1][0], data[2][0], self.data_source))
            )
        )
        return province_map

    def pieType(self, data)-> Pie:
        """
        -- 按列车类型统计车次数量
        :param data:list:[[X轴-类型名称], [Y轴-车次数量]]
        :return: Bar
        """
        type_pie = (
            Pie(init_opts=opts.InitOpts(width='1000px', height='500px'))
            .add("", data, radius=["30%", "75%"], center=["50%", "50%"], rosetype="radius",
                 label_opts=opts.LabelOpts(is_show=True))
            .set_global_opts(
                legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),
                title_opts=opts.TitleOpts(title='按列车类型统计车次数量',
                                          title_textstyle_opts=opts.TextStyleOpts(font_size=20),  # 设置标题大小
                                          subtitle='运行车次最多的是{}列车。{}'.format(data[0][0], self.data_source))
            )
        )
        return type_pie

    @staticmethod
    def barStartStation(data)-> Bar:
        """
        -- 按始发站统计车次数量
        :param data:list:[[X轴-始发站名称], [Y轴-车次数量]]
        :return: Bar
        """
        start_Station_bar = (
            Bar(init_opts=opts.InitOpts(width='1000px', height='500px'))
            .add_xaxis(data[0])
            .add_yaxis("车次数量", data[1], color='#9d2933')
            .set_global_opts(
                legend_opts=opts.LegendOpts(is_show=False),  # 不显示图例
                xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=30)),     # 横坐标标签倾斜
                yaxis_opts=opts.AxisOpts(name='次'),
                title_opts=opts.TitleOpts(title='全国始发列车最多的车站(TOP 20)',
                                          title_textstyle_opts=opts.TextStyleOpts(font_size=20))
            )
            .set_series_opts(
                label_opts=opts.LabelOpts(is_show=False),
                markline_opts=opts.MarkLineOpts(symbol='circle', precision=0,
                                                data=[opts.MarkLineItem(name='平均', type_='average')]),   # 平均值线
                markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max", name="Max"),
                                                        opts.MarkPointItem(type_="min", name="Min")]),
            )
        )
        return start_Station_bar

    @staticmethod
    def barEndStation(data)-> Bar:
        """
        -- 按终点站统计车次数量
        :param data:list:[[X轴-终点站名称], [Y轴-车次数量]]
        :return: Bar
        """
        end_Station_bar = (
            Bar(init_opts=opts.InitOpts(width='1000px', height='500px'))
            .add_xaxis(data[0])
            .add_yaxis("车次数量", data[1], color='#424c50')
            .set_global_opts(
                legend_opts=opts.LegendOpts(is_show=False),  # 不显示图例
                xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=30)),     # 横坐标标签倾斜
                yaxis_opts=opts.AxisOpts(name='次'),
                title_opts=opts.TitleOpts(title='全国终到列车最多的车站(TOP 20)',
                                          title_textstyle_opts=opts.TextStyleOpts(font_size=20))
            )
            .set_series_opts(
                label_opts=opts.LabelOpts(is_show=False),
                markline_opts=opts.MarkLineOpts(symbol='circle', precision=0,
                                                data=[opts.MarkLineItem(name='平均', type_='average')]),   # 平均值线
                markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max", name="Max"),
                                                        opts.MarkPointItem(type_="min", name="Min")]),
            )
        )
        return end_Station_bar

    @staticmethod
    def barStation(data)-> Bar:
        """
        -- 按经过列车统计车次数量
        :param data:list:[[X轴-车站名称], [Y轴-车次数量]]
        :return: Bar
        """
        station_bar = (
            Bar(init_opts=opts.InitOpts(width='1000px', height='500px'))
            .add_xaxis(data[0])
            .add_yaxis("车次数量", data[1], color='#057748')
            .set_global_opts(
                legend_opts=opts.LegendOpts(is_show=False),  # 不显示图例
                xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=30)),     # 横坐标标签倾斜
                yaxis_opts=opts.AxisOpts(name='次'),
                title_opts=opts.TitleOpts(title='全国经过列车最多的车站(TOP 20)',
                                          title_textstyle_opts=opts.TextStyleOpts(font_size=20))
            )
            .set_series_opts(
                label_opts=opts.LabelOpts(is_show=False),
                markline_opts=opts.MarkLineOpts(symbol='circle', precision=0,
                                                data=[opts.MarkLineItem(name='平均', type_='average')]),   # 平均值线
                markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max", name="Max"),
                                                        opts.MarkPointItem(type_="min", name="Min")]),
            )
        )
        return station_bar

    @staticmethod
    def barDistance(data)-> Bar:
        """
        -- 按运行里程区间统计车次数量
        :param data:list:[[X轴-里程区间], [Y轴-车次数量]]
        :return: Bar
        """
        distance_bar = (
            Bar(init_opts=opts.InitOpts(width='1000px', height='500px'))
            .add_xaxis(data[0])
            .add_yaxis("车次数量", data[1], color='#425066')
            .set_global_opts(
                legend_opts=opts.LegendOpts(is_show=False),  # 不显示图例
                xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=30), name='公里'),     # 横坐标标签倾斜
                yaxis_opts=opts.AxisOpts(name='次'),
                title_opts=opts.TitleOpts(title='按运行里程区间统计车次数量',
                                          title_textstyle_opts=opts.TextStyleOpts(font_size=20))
            )
            .set_series_opts(
                label_opts=opts.LabelOpts(is_show=False),
                markline_opts=opts.MarkLineOpts(symbol='circle', precision=0,
                                                data=[opts.MarkLineItem(name='平均', type_='average')]),   # 平均值线
                markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max", name="Max"),
                                                        opts.MarkPointItem(type_="min", name="Min")]),
            )
        )
        return distance_bar

    @staticmethod
    def barPeriod(data)-> Bar:
        """
        -- 按始终点运行时间统计车次数量
        :param data:list:[[X轴-运行时间区间], [Y轴-车次数量]]
        :return: Bar
        """
        period_bar = (
            Bar(init_opts=opts.InitOpts(width='1000px', height='500px'))
            .add_xaxis(data[0])
            .add_yaxis("车次数量", data[1], color='#7c4b00')
            .set_global_opts(
                legend_opts=opts.LegendOpts(is_show=False),  # 不显示图例
                xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=0), name='小时'),     # 横坐标标签倾斜
                yaxis_opts=opts.AxisOpts(name='次'),
                title_opts=opts.TitleOpts(title='按始终点运行时间统计车次数量',
                                          title_textstyle_opts=opts.TextStyleOpts(font_size=20))
            )
            .set_series_opts(
                label_opts=opts.LabelOpts(is_show=False),
                markline_opts=opts.MarkLineOpts(symbol='circle', precision=0,
                                                data=[opts.MarkLineItem(name='平均', type_='average')]),   # 平均值线
                markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max", name="Max"),
                                                        opts.MarkPointItem(type_="min", name="Min")]),
            )
        )
        return period_bar

    @staticmethod
    def barSpeed(data)-> Bar:
        """
        -- 按列车类型统计运行速度
        :param data:list:[[X轴-类型名称], [Y轴-速度]]
        :return: Bar
        """
        speed_bar = (
            Bar(init_opts=opts.InitOpts(width='1000px', height='500px'))
            .add_xaxis(data[0])
            .add_yaxis("车次数量", data[1], color='#8c4356')
            .set_global_opts(
                legend_opts=opts.LegendOpts(is_show=False),  # 不显示图例
                xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=0)),     # 横坐标标签倾斜
                yaxis_opts=opts.AxisOpts(name='公里/小时'),
                title_opts=opts.TitleOpts(title='按列车类型统计运行速度',
                                          title_textstyle_opts=opts.TextStyleOpts(font_size=20))
            )
            .set_series_opts(
                label_opts=opts.LabelOpts(is_show=False),
                markline_opts=opts.MarkLineOpts(symbol='circle', precision=0,
                                                data=[opts.MarkLineItem(name='平均', type_='average')]),   # 平均值线
                markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max", name="Max"),
                                                        opts.MarkPointItem(type_="min", name="Min")]),
            )
        )
        return speed_bar
