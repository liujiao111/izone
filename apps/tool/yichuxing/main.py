#! /usr/local/bin/python3
# coding: utf-8
# __author__ = "liujiao"
# __date__ = 2019/08/30 16:11

# 加载内置包
import requests
import json
from apps.tool.yichuxing import settings as settings
import time
import os
# 加载第三方包
import pandas
from apps.tool.yichuxing.proxy import getproxy
import apps.tool.yichuxing.transCoordinateSystem as  transCoordinateSystem
import glob

from queue import Queue #LILO队列


# TODO 输入坐标系：WGS84,输出坐标系：WGS84,宜出行用的是GCJ20坐标系，在程序中会转换两次

url = "https://c.easygo.qq.com/api/egc/heatmapdata"

edge = 2.6

lng_delta = 0.01167*edge
lat_delta = 0.009*edge

def spyder(params, cookie):


    user_header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "Referer": "http://c.easygo.qq.com/eg_toc/map.html?origin=csfw",
        "Cookie": cookie
    }

    try:
        r = requests.get(url, headers=user_header, params=params)

        #print("response code:", r.status_code, "response_text:", r.text)
        if r.status_code == 200:
            da = json.loads(r.text)
            if da['code'] == -100:
                # 出现验证码，换cookie
                return None, "出现验证码，当前cookie已不可用，请切换qq获取新的cookie!"
            if da['code'] == 3:
                # 当前cookie已过期，请重新登录
                return None, "当前cookie已过期，请重新登录后再试!"
            return r.text, "爬取成功"
        else:
            #出现验证码，换cookie
            return None, "爬取失败，宜出行返回状态码：" + r.status_code + ", 返回数据：" + r.text

    except Exception as e:
        print("发生异常", e)
        return None, "服务器爬取异常"

    return None, "服务器爬取异常"


def save(text, time_now, max_lon, min_lon, max_lat, min_lat, file_name):
    print('保存')
    try:
        with open(file_name, 'r') as f:
            f.readline()
    except FileNotFoundError as e:
        with open(file_name, 'w', encoding='utf-8') as f:
            #f.write('lat,lon,count\n')
            pass
    # 写入数据
    with open(file_name, "a", encoding="utf-8") as f:
        if text is None:
            return
        try:
            node_list = json.loads(text)["data"]
            min_count = json.loads(text)['max_data'] / 40
            for i in node_list:
                # 此处的算法在宜出行网页后台的js可以找到，文件路径是http://c.easygo.qq.com/eg_toc/js/map-55f0ea7694.bundle.js
                i['count'] = i['count'] / min_count
                lng = 1e-6 * (250.0 * i['grid_x'] + 125.0)
                lat = 1e-6 * (250.0 * i['grid_y'] + 125.0)
                lng, lat = transCoordinateSystem.gcj02_to_wgs84(lng, lat)
                print('过滤经纬度：', max_lon, min_lon)
                if max_lon != None and min_lon != "": #过滤坐标点
                    print('过滤...........')
                    print('当前经度,', str(lng), '过滤经纬度：', str(max_lon), str(min_lon), '当前纬度：', str(lat), '过滤纬度：', str(max_lat), str(min_lat))
                    if float(lng) <= float(max_lon) and float(lng) >= float(min_lon) and float(lat) <= float(max_lat) and float(lat) >= float(min_lat):
                        f.write(str(lat) + "," + str(lng) + "," + str(i['count']) + "\n")
                else:
                    f.write(str(lat) + "," + str(lng) + "," + str(i['count']) + "\n")
        except IndexError as e:
            pass
            # print("此区域没有点信息")
        except TypeError as e:
            print(node_list)
        except Exception as e:
            print('发生错误:', text, file_name)
            return

def remove_duplicate(filepath):
    #df = pandas.read_csv(filepath,sep=",")
    time_now1 = time.time()
    try:
        df = pandas.read_csv(filepath, sep=',')
        df = df.drop_duplicates()
        csv_name = filepath.replace(".txt", "-result-" + str(time_now1) + ".csv")
        df.to_csv(csv_name, index=False)
    except Exception as e:
        print('当前爬取的数据为空...')



# 读取网格数据，分别爬取
# 初始化用于爬虫的网格，形成url
def initial_paramslist(points):
    """
    :return: List[]
    """
    round = []
    for point in str(points).split(';'):
        if(point == None or point == ""):
            continue
        lng, lat = float(point.split(",")[0]), float(point.split(",")[1])
        round.append([lng - 0.5 * lng_delta,
                      lng + 0.5 * lng_delta,
                      lat - 0.5 * lat_delta,
                      lat + 0.5 * lat_delta])


    # 生成待抓取的params
    paramslist = []
    for item in round:
        lng_min, lng_max, lat_min, lat_max = item
        lng_min, lat_min = transCoordinateSystem.wgs84_to_gcj02(lng_min, lat_min)
        lng_max, lat_max = transCoordinateSystem.wgs84_to_gcj02(lng_max, lat_max)
        params = {"lng_min": lng_min,
                  "lat_max": lat_max,
                  "lng_max": lng_max,
                  "lat_min": lat_min,
                  "level": 16,
                  "city": "厦门",
                  "lat": "undefined",
                  "lng": "undefined",
                  "_token": ""}
        paramslist.append(params)
    return paramslist



def get_data(ycx_points, cookie, max_lon, min_lon, max_lat, min_lat):
    params_list = initial_paramslist(ycx_points)

    #创建一个文件夹用来保存当次爬取的数据
    time_now1 = time.time()
    time_now1 = time.strftime('%Y-%m-%d-%H-%M', time.localtime(time_now1))
    current_file_path = settings.filepath + time_now1 + "/"
    if os.path.exists(current_file_path) is False:
        os.makedirs(current_file_path)


    index = 1

    for params in params_list:

        # 2.抓取单个网格数据
        print("=================第" + str(index) + "个网格爬取开始...........")

        data, msg = spyder(params, cookie)
        if data is None:
            print('本次网格爬取失败,当前网格数： '+ str(index) + ", params:" +  str(params))
            return msg, 500

        # 3.数据处理，并入库
        time_now = time.time()
        time_now_str = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time_now))
        save(data, time_now_str, max_lon, min_lon, max_lat, min_lat , file_name=current_file_path + settings.filename + time_now_str + ".txt")
        # 4.去重,并处理为CSV格式
        remove_duplicate(current_file_path + settings.filename + time_now_str + ".txt")

        #睡一觉再说
        #time.sleep(100)
        index = index + 1

    #合并全部CSV文件为一个CSV文件
    csv_list = glob.glob(current_file_path + "/" + '*.csv')  # 查看同文件夹下的csv文件数
    print(u'共发现%s个CSV文件' % len(csv_list))
    print(u'正在处理............')
    now_time_str = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    filename = 'heatdata-'+now_time_str+'.csv'
    file_name = current_file_path + "/" + filename
    for i in csv_list:  # 循环读取同文件夹下的csv文件
        fr = open(i, 'rb').read()
        with open(file_name, 'ab') as f:  # 将结果保存为result.csv
            f.write(fr)
    df = pandas.read_csv(file_name, sep=',')
    df = df.drop_duplicates()
    df.to_csv(file_name, index=False, header=['lat', 'lon', 'count'])
    print(u'合并完毕！')
    print('爬取完成，文件所在路径：' + file_name)

    #删除目录下的所有无用文件
    for i in csv_list:
        if i is not file_name:
            if os.path.exists(i):
                os.remove(i)
    txt_list = glob.glob(current_file_path + "/" + '*.txt')  # 查看同文件夹下的csv文件数
    for j in txt_list:
        if os.path.exists(j):
            os.remove(j)

    return file_name, 200


