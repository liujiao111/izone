import requests
import logging
import pandas as pd
import uuid
import os
import csv

GMAP_WEB_KEY = '0569ee1606c59bb225af54fc2a81b2e3'
GEO_CODE_BASE_URL = 'https://restapi.amap.com/v3/geocode/geo' #?address={address}&key={amap_key}




def get_geo_info_by_address(address):
    '''
    根据地址反查经纬度信息
    :param address: 结构化地址
    :return:
    '''
    req_url = GEO_CODE_BASE_URL + '?address=%s&}&key=%s' % (address, GMAP_WEB_KEY)
    try:
        response = requests.get(req_url)
        if response.status_code == requests.codes.ok:
            return response.json()
        logging.error('get invalid status code %s while scraping %s', response.status_code, req_url)
    except requests.RequestException:
        logging.error('error occurred while scraping %s', req_url, exc_info=True) # exc_info 参数设置为 True 则可以打印出 Traceback 错误堆栈信息。
    return None



def geo_address(csv_file_path):

    #读取csv文件
    csv_file = pd.read_csv(csv_file_path, encoding='utf_8_sig')

    file_name = str(uuid.uuid4()).replace("-", "") + ".csv"
    new_file_name = "data" + os.sep + "upload" + os.sep + file_name
    #new_file_path = os.path.abspath(os.getcwd()) + os.sep + new_file_name

    new_file_path = 'C:\\Users\\hgvgh\\Desktop\\blog\\izone\\apps\\tool' + os.sep + file_name

    file = open(new_file_path, 'w', newline='')
    writer = csv.writer(file)
    writer.writerow(['adcode', 'city', 'citycode', 'country', 'district', 'formatted_address', 'level', 'lng', 'lat', 'number', 'province', 'street'])

    for i in range(len(csv_file)):
        address = csv_file['address'][i]
        geo_info = get_geo_info_by_address(address)
        print(geo_info)
        if geo_info:
            if geo_info.get('status') == '1':
                geocodes = geo_info.get('geocodes')
                if len(geocodes) > 0:
                    first_address_info = geocodes[0]
                    adcode = first_address_info.get('adcode')
                    city = first_address_info.get('city')
                    citycode = first_address_info.get('citycode')
                    country = first_address_info.get('country')
                    district = first_address_info.get('district')
                    formatted_address = first_address_info.get('formatted_address')
                    level = first_address_info.get('level')
                    location = first_address_info.get('location')
                    number = first_address_info.get('number')
                    province = first_address_info.get('province')
                    street = first_address_info.get('street')
                    lng = location.split(',')[0]
                    lat = location.split(',')[1]

                    writer.writerow([adcode, city, citycode, country, district, formatted_address, level, lng, lat, number, province, street])
    return new_file_path

if __name__ == '__main__':
    print(geo_address('qq.csv'))