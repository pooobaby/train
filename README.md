# Train
全国铁路旅客列车数据可视化项目

## 项目文件

* 【create_station_geo.py】:根据火车站的基础数据生成全国所有火车站的地理位置信息    
    * In：.data\station_base.txt：全国所有火车站基础数据文件
    * Out：.data\invalid_station.csv：不能生成地理位置信息的火车站信息文件
* 【create_train_json.py】:根据12306获取的所有车次信息基础数据提取所有车次信息和车次代号  
    * In：.data\train_base.json：全国所有车次基础数据文件
    * Out：.data\train.json：从基础数据中提取的全国所有车次数据文件
* 【get_train.py】:根据车次信息爬取列车详细信息并保存到数据库中
    * In：.data\train.json：全国所有车次数据文件
    * Out：
        * .data\invalid_train.txt：不能获取到详细信息的车次数据文件
        * .data\train_logging.log：获取车次详细信息时生成的日志文件
        
## 项目说明

* 车次基础数据来源：12306.cn（2019年11月数据）
* 车次详细信息来源：oklx.com(12306爬取速度太慢)
* 数据存储：mongoDB
* 获取车站基础数据2992个，生成有效地理位置数据2830个
* 获取获取车次基础数据共8314次，最终获取8220次
