from urllib.parse import quote
from urllib import request
import json
import xlwt
from xpinyin import Pinyin
import os
from apps.tool.transCoordinateSystem import gcj02_to_wgs84, gcj02_to_bd09
import  apps.tool.distrinct as  distrinct
import xlrd
import pandas as pd

# TODO 替换为上面申请的密钥
poi_search_url = "http://restapi.amap.com/v3/place/text"
poi_boundary_url = "https://ditu.amap.com/detail/get/detail"


GMAP_KEY = '86e468edba1416f571f345d60a577220'

poi_xingzheng_distrinct_url = "https://restapi.amap.com/v3/config/district?subdistrict=1&key=" + GMAP_KEY
# from transCoordinateSystem import gcj02_to_wgs84


# 根据城市名称和分类关键字获取poi数据
def getpois(cityname, keywords, key):
    i = 1
    poilist = []
    while True:  # 使用while循环不断分页获取数据
        result = getpoi_page(cityname, keywords, i, key)
        print(result)
        result = json.loads(result)  # 将字符串转换为json
        if result['count'] == '0':
            break
        hand(poilist, result)
        i = i + 1
    return poilist


# 数据写入excel
def write_to_excel(poilist, cityname, classfield, coord):
    # 一个Workbook对象，这就相当于创建了一个Excel文件
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet(classfield, cell_overwrite_ok=True)

    # 第一行(列标题)
    sheet.write(0, 0, 'lon')
    sheet.write(0, 1, 'lat')
    sheet.write(0, 2, 'name')
    sheet.write(0, 3, 'address')
    sheet.write(0, 4, 'pname')
    sheet.write(0, 5, 'cityname')
    sheet.write(0, 6, 'business_area')
    sheet.write(0, 7, 'type')
    sheet.write(0, 8, 'id')
    sheet.write(0, 9, 'tel')

    for i in range(len(poilist)):
        location = poilist[i]['location']
        name = poilist[i]['name']
        address = poilist[i]['address']
        pname = poilist[i]['pname']
        cityname = poilist[i]['cityname']
        business_area =  poilist[i]['business_area']
        type = poilist[i]['type']
        tel = poilist[i]['tel']
        id = poilist[i]['id']
        lng = str(location).split(",")[0]
        lat = str(location).split(",")[1]

        if(coord == "2"):
            result = gcj02_to_wgs84(float(lng), float(lat))
            lng = result[0]
            lat = result[1]
        if(coord == "3"):
            result = gcj02_to_bd09(float(lng), float(lat))
            lng = result[0]
            lat = result[1]

        # 每一行写入
        sheet.write(i + 1, 0, lng)
        sheet.write(i + 1, 1, lat)
        sheet.write(i + 1, 2, name)
        sheet.write(i + 1, 3, address)
        sheet.write(i + 1, 4, pname)
        sheet.write(i + 1, 5, cityname)
        sheet.write(i + 1, 6, business_area)
        sheet.write(i + 1, 7, type)
        sheet.write(i + 1, 8, id)
        sheet.write(i + 1, 9, tel)


    # 最后，将以上操作保存到指定的Excel文件中
    p = Pinyin()
    p.get_pinyin(cityname)
    path = "data/poi/" + p.get_pinyin(cityname) + "-" + p.get_pinyin(classfield) + '.xls'
    book.save(r'' + os.getcwd() + "/" + path)
    return path


# 将返回的poi数据装入集合返回
def hand(poilist, result):
    # result = json.loads(result)  # 将字符串转换为json
    pois = result['pois']
    for i in range(len(pois)):
        poilist.append(pois[i])


# 单页获取pois
def getpoi_page(cityname, keywords, page, key):
    req_url = poi_search_url + "?key=" + key + '&extensions=all&keywords=' + quote(
        keywords) + '&city=' + quote(cityname) + '&citylimit=true' + '&offset=25' + '&page=' + str(
        page) + '&output=json'
    data = ''
    with request.urlopen(req_url) as f:
        data = f.read()
        data = data.decode('utf-8')
    return data


def get_areas(code):
    '''
    获取城市的所有区域
    :param code:
    :return:
    '''

    print('获取城市的所有区域：code: ' + str(code).strip())
    data = get_distrinctNoCache(code)

    print('get_distrinct result:' + data)

    data = json.loads(data)
    districts = data['districts'][0]['districts']
    i = 0
    area = ""
    for district in districts:
        name = district['name']
        adcode = district['adcode']
        i = i + 1
        area = area + "," + adcode

    print(area)
    print(str(area).strip(','))
    return str(area).strip(',')


def get_data(province, city, keyword, coord, key):
    isNeedAreas = True
    if(province == "820000" or province == "810000" or province == "500000" or province == "310000"
     or province == "710000"):  #310000
        area = province
        isNeedAreas = False

    #如果不是直辖市，需要获取城市的区域
    if isNeedAreas:
        area = get_areas(city)

    city = str(city)
    coord = str(coord)
    key = str(key)
    all_pois = []
    if (area != None and area != ""):
        area_list = str(area).split(",")
        if area_list == 0:
            area_list = str(area).split("，")

        for area in area_list:
            pois_area = getpois(area, keyword, key)
            print('当前城区：' + str(area) + ', 分类：' + str(keyword) + ", 总的有" + str(len(pois_area)) + "条数据")
            all_pois.extend(pois_area)
        print("所有城区的数据汇总，总数为：" + str(len(all_pois)))
        #return write_to_excel(all_pois, city, keyword, coord)
        return write_to_csv(all_pois, city, keyword, coord)
    else:
        pois_area = getpois(area, keyword)
        #return write_to_excel(pois_area, city, keyword, coord)
        return write_to_csv(pois_area, city, keyword, coord)

    return None


# 数据写入csv文件中
def write_to_csv(poilist, cityname, classfield, coord):
    data_csv = {}
    ids, lons, lats, names, addresss, pnames, citynames, business_areas, types, tels = [], [], [], [], [], [], [], [], [], []

    for i in range(len(poilist)):
        id = poilist[i]['id']
        location = poilist[i]['location']
        name = poilist[i]['name']
        address = poilist[i]['address']
        pname = poilist[i]['pname']
        cityname = poilist[i]['cityname']
        business_area = poilist[i]['business_area']
        type = poilist[i]['type']
        tel = poilist[i]['tel']
        lng = str(location).split(",")[0]
        lat = str(location).split(",")[1]

        if (coord == "2"):
            result = gcj02_to_wgs84(float(lng), float(lat))
            lng = result[0]
            lat = result[1]
        if (coord == "3"):
            result = gcj02_to_bd09(float(lng), float(lat))
            lng = result[0]
            lat = result[1]
        ids.append(id)
        lons.append(lng)
        lats.append(lat)
        names.append(name)
        addresss.append(address)
        pnames.append(pname)
        citynames.append(cityname)
        if business_area == []:
            business_area = ''
        business_areas.append(business_area)
        types.append(type)
        tels.append(tel)
    data_csv['id'], data_csv['lon'], data_csv['lat'], data_csv['name'], data_csv['address'], data_csv['pname'], \
    data_csv['cityname'], data_csv['business_area'], data_csv['type'], data_csv['tel'] = \
        ids, lons, lats, names, addresss, pnames, citynames, business_areas, types, tels

    df = pd.DataFrame(data_csv)

    # 最后，将以上操作保存到指定的Excel文件中
    p = Pinyin()
    p.get_pinyin(cityname)
    path = "data/poi/" + p.get_pinyin(cityname) + "-" + p.get_pinyin(classfield) + '.csv'
    df.to_csv(os.getcwd() + "/" + path, index=False, encoding='utf_8_sig')
    return path


def get_distrinctNoCache(code):
        '''
        获取中国城市行政区划
        :return:
        '''

        url = "https://restapi.amap.com/v3/config/district?subdistrict=2&extensions=all&key=" + GMAP_KEY

        print(url + "&keywords=" + code)

        with request.urlopen(url + "&keywords=" + code) as f:
            data = f.read()
            data = data.decode('utf-8')
        print(code, data)
        return data


def get_distrinct(code):
    '''
    获取中国城市行政区划
    :return:
    '''

    print(poi_xingzheng_distrinct_url + "&keywords=" + code)

    #从本地缓存文件中获取数据，避免每次调用接口，体验太差
    distrinct_code = "DISTRINCT_" + str(code)
    if distrinct.distrincts.get(distrinct_code) is not "":
        print("=====================已经缓存到本地，无需调用接口=====================")
        print('缓存返回数据：' + str(distrinct.distrincts.get(distrinct_code)))
        return distrinct.distrincts.get(distrinct_code)


    with request.urlopen(poi_xingzheng_distrinct_url + "&keywords=" + code) as f:
        data = f.read()
        data = data.decode('utf-8')

    #将获取到的数据缓存到本地
    distrinct.distrincts[distrinct_code] = data
    print(code, data)
    return data







def get_poi_map_data(filepath):
    '''
    读取PEXCEL格式的POI数据，转换为百度地图可视化需要的数据格式
    :param filepath:
    :return:
    '''
    workbook = xlrd.open_workbook(filename=filepath)
    sheet_first = workbook.sheets()[0]

    result = []
    for i in range(1, sheet_first.nrows):
        lon, lat, name = sheet_first.cell_value(i, 0), sheet_first.cell_value(i, 1), sheet_first.cell_value(i, 2)
        ls = []
        ls.append(lon)
        ls.append(lat)
        ls.append(name)
        result.append(ls)
    return result





'''
data = get_distrinct("620500")
data = json.loads(data)
print(data)
districts = data['districts'][0]['districts']
i= 0
for district in districts:
    name = district['name']
    adcode = district['adcode']
    #print('<option value="'+ adcode+'">'+name+'</option>')
    i = i+ 1
#print(i)
    #<option value="150000">内蒙古自治区</option>
    '''
