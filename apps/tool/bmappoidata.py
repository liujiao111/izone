#coding: utf-8
import requests
import json
import time
import os
import pandas as pd
from apps.tool.transCoordinateSystem import bd09_to_gcj02, bd09_to_wgs84


"""
    查询关键字：
"""
#KeyWord = u"住宅区"
#baiduAk = '1QkdIjutWv0jBDZEKqy9TH4O3divaRcS'
"""
    关注区域的左下角和右上角百度地图坐标(经纬度）
"""

'''
BigRect = {
    'left': {

        'x': 113.80650422835264,
        'y': 22.4897508735693
    },
    'right': {
        'x': 114.21980273738981,
        'y': 22.803672722381442
    }
}
'''

"""
    定义细分窗口的数量，横向X * 纵向Y
"""


WindowSize = {
    'xNum': 10.0,
    'yNum': 10.0
}




def getSmallRect(bigRect, windowSize, windowIndex):
    """
    获取小矩形的左上角和右下角坐标字符串（百度坐标系）
    :param bigRect: 关注区域坐标信息
    :param windowSize:  细分窗口数量信息
    :param windowIndex:  Z型扫描的小矩形索引号
    :return: lat,lng,lat,lng
    """
    offset_x = (bigRect['right']['x'] - bigRect['left']['x'])/windowSize['xNum']
    offset_y = (bigRect['right']['y'] - bigRect['left']['y'])/windowSize['yNum']
    left_x = bigRect['left']['x'] + offset_x * (windowIndex % windowSize['xNum'])
    left_y = bigRect['left']['y'] + offset_y * (windowIndex // windowSize['yNum'])
    right_x = (left_x + offset_x)
    right_y = (left_y + offset_y)
    return str(left_y) + ',' + str(left_x) + ',' + str(right_y) + ',' + str(right_x)


def requestBaiduApi(keyWords, smallRect, baiduAk):
    pageNum = 0
    file = open(os.getcwd() + os.sep + "data/result.txt", 'a+', encoding='utf-8')
    pois = []
    while True:
        try:
            URL = "http://api.map.baidu.com/place/v2/search?query=" + keyWords + \
                "&bounds=" + smallRect + \
                "&output=json" +  \
                "&ak=" + baiduAk + \
                "&scope=2" + \
                "&page_size=20" + \
                "&page_num=" + str(pageNum)
            print(pageNum)
            print(URL)
            resp = requests.get(URL)
            res = json.loads(resp.text)
            # print(resp.text.strip())
            if len(res['results']) == 0:
                print('返回结果为0')
                break
            else:
                for r in res['results']:
                    pois.append(r)
                    file.writelines(str(r).strip() + '\n')
            pageNum += 1
            time.sleep(1)
        except:
            print("except")
            break
    return pois




def get_bmap_data(max_lon, min_lon, max_lat, min_lat, KeyWord, coord, baiduAk):
    BigRect = {
        'left': {

            'x': min_lon,
            'y': min_lat
        },
        'right': {
            'x': max_lon,
            'y': max_lat
        }
    }
    all_pois = []
    for index in range(int(WindowSize['xNum'] * WindowSize['yNum'])):
        smallRect = getSmallRect(BigRect, WindowSize, index)
        #print("第" + str(index) + "个网格", smallRect)
        #continue
        pois = requestBaiduApi(keyWords=KeyWord, smallRect=smallRect, baiduAk=baiduAk)
        all_pois.extend(pois)
        time.sleep(1)
    #return
    data_csv = {}
    uids, names, provinces, citys, areas, addresses, lngs, lats = [], [], [], [], [], [], [], []
    for poi in all_pois:
        if poi == None:
            continue
        if 'uid' in poi:
            uids.append(poi['uid'])
        else:
            uids.append('')
        if 'name' in poi:
            names.append(poi['name'])
        else:
            names.append('')
        if 'province' in poi:
            provinces.append(poi['province'])
        else:
            provinces.append('')
        if 'city' in poi:
            citys.append(poi['city'])
        else:
            citys.append('')
        if 'area' in poi:
            areas.append(poi['area'])
        else:
            areas.append('')

        if 'address' in poi:
            addresses.append(poi['address'])
        else:
            addresses.append('')
        location = poi['location']
        lng = location['lng']
        lat = location['lat']


        if (coord == "1"):
            result = bd09_to_gcj02(float(lng), float(lat))
            lng = result[0]
            lat = result[1]
        if (coord == "2"):
            result = bd09_to_wgs84(float(lng), float(lat))
            lng = result[0]
            lat = result[1]

        lngs.append(lng)
        lats.append(lat)

    data_csv['uid'] = uids
    data_csv['name'] = names
    data_csv['province'] = provinces
    data_csv['city'] = citys
    data_csv['area'] = areas
    data_csv['address'] = addresses
    data_csv['lng'] = lngs
    data_csv['lat'] = lats

    df = pd.DataFrame(data_csv)
    df.to_csv(os.getcwd() + os.sep + 'data/bmap-poi-' + KeyWord + '.csv', index=False, encoding='gbk')

