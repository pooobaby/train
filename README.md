# Train
全国铁路旅客列车数据可视化项目

## 基础数据来源：

* 【trains_base.json】:车次基础数据，来源：12306.cn（2019年11月数据）
* 【station_base.csv】:车站基础数据，来源：12306.cn，获取详细车次信息后增加近500个

## 项目文件

* 【get_telecode.py】:根据车站基础数据在moerail.ml获取包含电报码的车站初步信息
    * In：
        * data\station_base.csv，车站基础数据
    * Out：
        * data\logging_telecode.log：日志文件
        * mongoDB.train.StationTelecode：存储包含电报码的车站初步信息集合
* 【create_station_geo.py】:根据车站初步信息生成地理位置信息    
    * In：
        * mongoDB.train.StationTelecode：存储车站详细信息的集合
    * Out：
        * data\logging_geo.log：日志文件，部分车站需要手支输入
        * mongoDB.train.StationGeo：存储车站地理位置信息的集合
* 【create_train_json.py】:根据车次基础数据提取所有车次信息和车次代号  
    * In：
        * data\train_base.json：车次基础数据
    * Out：
        * data\train.json：从基础数据中提取的全国所有车次数据文件
* 【get_traininfo.py】:根据车次信息爬取列车详细信息并保存到数据库中
    * In：
        * data\train.json：全国所有车次数据文件
    * Out：
        * data\invalid_train.txt：不能获取到详细信息的车次数据文件
        * data\logging_train.log：日志文件
        * mongoDB.train.Train：存储车次详细信息的集合
* 【clean_data.py】:根据车次详细信息进行数据处理
    * In:
        * mongoDB.train.Train：存储车次详细信息的集合
    * Out:
        * 按类型
        * 始发站(TOP 20)
        * 终到站(TOP 20)
        * 所有车站经过列车(TOP 20)
        * 各里程区间运行的列车数量
        * 车次运行里程最长(TOP 20)
        * 车次运行里程最短(TOP 20)
        * 各类型车次运行里程最长(TOP 20)
        * 各时长区间运行的列车数量(TOP 10)
        * 运行时间最长的列车(TOP 20)
        * 运行时间最短的列车(TOP 20)
        * 各类型运行平均速度
        
## 项目说明

* 车次基础数据来源：12306.cn（2019年11月数据）
* 车次详细信息来源：oklx.com(12306爬取速度太慢)
* 车站电报码信息来源：moerail.ml
* 数据存储：mongoDB
* 获取车站基础数据3480个，生成有效地理位置数据3480个
* 获取获取车次基础数据共8314次，最终获取8220次，去重后8217次
