import pandas as pd
import os
import requests
import json
from requests.adapters import HTTPAdapter
import uuid


def get_boundary_by_uid(uid, bmap_key):
    bmap_boundary_url = 'https://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=ext&uid=' + uid + '&c=340&ext_ver=new&tn=B_NORMAL_MAP&nn=0&auth=fw9wVDQUyKS7%3DQ5eWeb5A21KZOG0NadNuxHNBxBBLBHtxjhNwzWWvy1uVt1GgvPUDZYOYIZuEt2gz4yYxGccZcuVtPWv3GuxNt%3DkVJ0IUvhgMZSguxzBEHLNRTVtlEeLZNz1%40Db17dDFC8zv7u%40ZPuxtfvSulnDjnCENTHEHH%40NXBvzXX3M%40J2mmiJ4Y&ie=utf-8&l=19&b=(12679382.095,2565580.38;12679884.095,2565907.38)&t=1573133634785'

    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=3))
    s.mount('https://', HTTPAdapter(max_retries=3))

    data = s.get(url=bmap_boundary_url, timeout=5, headers={"Connection": "close"})
    data = data.text
    print(bmap_boundary_url, data)
    data = json.loads(data)
    content = data['content']
    if not 'geo' in content:
        print('geo is not in content')
        return None
    geo = content['geo']
    i = 0
    strsss = ''
    for jj in str(geo).split('|')[2].split('-')[1].split(','):
        jj = str(jj).strip(';')
        if i % 2 == 0:
            strsss = strsss + str(jj) + ','
        else:
            strsss = strsss + str(jj) + ';'
        i = i + 1
    return strsss.strip(";")

def transform_coordinate_batch(coordinates, bmap_key):
    req_url = 'http://api.map.baidu.com/geoconv/v1/?coords='+coordinates+'&from=6&to=5&ak=' + bmap_key

    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=3))
    s.mount('https://', HTTPAdapter(max_retries=3))

    data = s.get(req_url, timeout=5, headers={"Connection": "close"})  # , proxies=proxies
    data = data.text
    data = json.loads(data)
    coords = ''
    if data['status'] == 0:
        result = data['result']
        if len(result) > 0:
            for res in result:
                lng = res['x']
                lat = res['y']
                coords = coords + ";" + str(lng) + "," + str(lat)
    return coords.strip(";")



def get_boundary(csv_file_path, bmap_key):
    print('文件地址：', csv_file_path)
    csv_file = pd.read_csv(csv_file_path, encoding='utf_8_sig')
    data_csv = {}
    uids, boundarys = [], []
    for i in range(len(csv_file)):
        uid = ''
        try:
            uid = csv_file['uid'][i]
            uids.append(uid)
            coordinates = get_boundary_by_uid(uid, bmap_key)
            if coordinates is not None:
                coords = transform_coordinate_batch(coordinates, bmap_key)
                print('成功返回边界：', uid + ',' + coords)
                boundarys.append(coords)
            else:
                boundarys.append(' ')
        except Exception:
            uids.append(uid)
            boundarys.append(' ')

    data_csv['uid'] = uids
    data_csv['boundary'] = boundarys
    df = pd.DataFrame(data_csv)
    csv_file_path = os.getcwd() + os.sep + 'data/' + str(uuid.uuid4()).replace("-", "") +'.csv'

    df.to_csv(csv_file_path, index=False, encoding='gbk')
    return csv_file_path


def parse_boundary(filename):
    '''
    将边界坐标处理为ARCGIS可展示的数据格式
    :return:
    '''

    csv_file = pd.read_csv(filename, encoding='gbk')

    data_csv = {}
    numbers, xs, ys, uids = [], [], [], []
    index = 1
    for i in range(len(csv_file)):
        boundary = str(csv_file['boundary'][i])
        uid = str(uuid.uuid4()).replace('-', '')

        if boundary is not ' ':
            print('boundary is not null')
            for point in boundary.split(";"):
                lng = point.split(",")[0]
                lat = point.split(",")[1]
                xs.append(lng)
                ys.append(lat)
                numbers.append(index)
                uids.append(uid)

                index = index + 1
    data_csv['number'] = numbers
    data_csv['x'] = xs
    data_csv['y'] = ys
    data_csv['uid'] = uids

    df = pd.DataFrame(data_csv)
    csv_file_path = os.getcwd() + os.sep + 'data/' + str(uuid.uuid4()).replace("-", "") + '.csv'
    df.to_csv(csv_file_path, index=False, encoding='gbk')
    return csv_file_path
