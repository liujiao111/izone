import xlrd
from xlutils.copy import copy
import os
import pandas as pd
import uuid

from apps.tool.transCoordinateSystem import gcj02_to_wgs84, gcj02_to_bd09, wgs84_to_gcj02, wgs84_to_bd09, bd09_to_gcj02, bd09_to_wgs84

def transfer(orgcoord, targetcoord, filename):
    '''
    坐标转换
    默认第一二列为经纬度
    :param filename:
    :return:
    '''
    workbook = xlrd.open_workbook(filename, encoding_override='utf_8_sig')
    new_workbook = copy(workbook)
    new_worksheet = new_workbook.get_sheet(0)
    sheet = workbook.sheets()[0]


    target_col_name = 'gcj20'
    if targetcoord == "2":
        target_col_name = 'wgs84'
    elif targetcoord == "3":
        target_col_name = 'bd09'


    for i in range(1, sheet.nrows):
        lon, lat = sheet.cell_value(i, 0), sheet.cell_value(i, 1)
        # 坐标转换
        if orgcoord == "1":
            if targetcoord == "1":
                pass
            elif targetcoord == "2":
                print('高德->WGS84坐标系，', lon, lat)

                result = gcj02_to_wgs84(float(lon), float(lat))
                lon = result[0]
                lat = result[1]

                print('高德->WGS84坐标系结果：', lon, lat)

            elif targetcoord == "3":
                result = gcj02_to_bd09(float(lon), float(lat))
                lon = result[0]
                lat = result[1]
        elif orgcoord == "2":
            if targetcoord == "1":
                result = wgs84_to_gcj02(float(lon), float(lat))
                lon = result[0]
                lat = result[1]
            elif targetcoord == "2":
                pass
            elif targetcoord == "3":
                result = wgs84_to_bd09(float(lon), float(lat))
                lon = result[0]
                lat = result[1]

        elif orgcoord == "3":
            if targetcoord == "1":
                result = bd09_to_gcj02(float(lon), float(lat))
                lon = result[0]
                lat = result[1]
            elif targetcoord == "2":
                result = bd09_to_wgs84(float(lon), float(lat))
                lon = result[0]
                lat = result[1]
            elif targetcoord == "3":
                pass

        new_worksheet.write(i, sheet.ncols + 1, lon)
        new_worksheet.write(i, sheet.ncols + 2, lat)

    new_worksheet.write(0, sheet.ncols + 1, 'lon-' + target_col_name)
    new_worksheet.write(0, sheet.ncols + 2, 'lat-' + target_col_name)
    file_name = str(uuid.uuid4()).replace("-", "") + "."
    new_file_name = "data/upload/" + file_name
    new_file_path = os.path.abspath(os.getcwd()) + "/" + new_file_name
    new_workbook.save(new_file_path)  # 保存工作簿
    return new_file_name


def coord_check(orgcoord, targetcoord, lon, lat):
    if orgcoord == "1":
        if targetcoord == "1":
            lon, lat = lon, lat
        elif targetcoord == "2":
            result = gcj02_to_wgs84(float(lon), float(lat))
            lon = result[0]
            lat = result[1]

        elif targetcoord == "3":
            result = gcj02_to_bd09(float(lon), float(lat))
            lon = result[0]
            lat = result[1]
    elif orgcoord == "2":
        if targetcoord == "1":
            result = wgs84_to_gcj02(float(lon), float(lat))
            lon = result[0]
            lat = result[1]
        elif targetcoord == "2":
            lon, lat = lon, lat
        elif targetcoord == "3":
            result = wgs84_to_bd09(float(lon), float(lat))
            lon = result[0]
            lat = result[1]

    elif orgcoord == "3":
        if targetcoord == "1":
            result = bd09_to_gcj02(float(lon), float(lat))
            lon = result[0]
            lat = result[1]
        elif targetcoord == "2":
            result = bd09_to_wgs84(float(lon), float(lat))
            lon = result[0]
            lat = result[1]
        elif targetcoord == "3":
            lon, lat = lon, lat
    return [lon, lat]

def transfer_csv(orgcoord, targetcoord, filename):
    '''
    坐标转换，文件类型为CSV
    :param orgcoord:
    :param targetcoord:
    :param filename:
    :return:
    '''
    data = pd.read_csv(filename, encoding='utf_8_sig')
    lons = data['lon']
    lats = data['lat']
    for i in range(len(lons)):
        print(lons[i])

    new_coord_lon, new_coord_lat = [], []

    target_col_name = 'gcj20'
    if targetcoord == "2":
        target_col_name = 'wgs84'
    elif targetcoord == "3":
        target_col_name = 'bd09'


    for i in range(len(lons)):
        lon = lons[i]
        lat = lats[i]
        #print(lon, lat)
        location = coord_check(orgcoord, targetcoord, lon, lat)
        lon, lat = location[0], location[1]
        new_coord_lon.append(lon)
        new_coord_lat.append(lat)

    new_coord_lon = pd.Series(new_coord_lon)
    new_coord_lat = pd.Series(new_coord_lat)

    data['lon-' + target_col_name] = new_coord_lon
    data['lat-' + target_col_name] = new_coord_lat
    file_name = str(uuid.uuid4()).replace("-", "") + ".csv"
    new_file_name = "data/upload/" + file_name
    new_file_path = os.path.abspath(os.getcwd()) + "/" + new_file_name
    data.to_csv(new_file_path, mode='a', index=False)
    return new_file_name


