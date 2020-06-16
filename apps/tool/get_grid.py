from apps.tool.get_distance import get_distance
#TODO
require_distance = 2.6#要求的地图网格间隔距离(千米为单位)  -- 百度地图

import uuid
import os


def get_ss (point_A, point_D, point_B, point_C, require_distance = 2.5):

    # AB间的距离
    distance_AB = get_distance(point_A[1], point_A[0], point_B[1], point_B[0])
    # print(distance_AB) #13.381562710218205

    # AD间的距离
    distance_AD = get_distance(point_A[1], point_A[0], point_D[1], point_D[0])
    # print(distance_AD) #7.735240077970707

    # AB边上平分点的个数
    num_split_AB = int(
        distance_AB / require_distance if distance_AB % require_distance == 0 else distance_AB // require_distance + 1) - 1
    # print('AB边上平分点的个数', str(num_split_AB))

    # AD边上评分的个数
    num_split_AD = int(
        distance_AD / require_distance if distance_AD % require_distance == 0 else distance_AD // require_distance + 1) - 1
    # print('AD边上评分的个数', str(num_split_AD))

    # 计算AB线段上各个点的坐标
    points_coordinate_AB = []
    for i in range(num_split_AB + 1):
        x = point_A[0] + (point_B[0] - point_A[0]) / (num_split_AB + 1) * i
        y = point_A[1] + (point_B[1] - point_A[1]) / (num_split_AB + 1) * i
        points_coordinate_AB.append([x, y])
    points_coordinate_AB.append(point_B)  # 加上B点的坐标
    # print('AB线段上各个平分点的坐标集合：', points_coordinate_AB)

    # 计算DC线段上各个点的坐标
    points_coordinate_DC = []
    for i in range(num_split_AB + 1):
        x = point_D[0] + (point_C[0] - point_D[0]) / (num_split_AB + 1) * i
        y = point_D[1] + (point_C[1] - point_D[1]) / (num_split_AB + 1) * i
        points_coordinate_DC.append([x, y])
    points_coordinate_DC.append(point_C)  # 加上B点的坐标
    # print('DC线段上各个平分点的坐标集合：', points_coordinate_DC)

    # 计算中间网格交汇点坐标
    points_coordinate_result = []
    strtt = ""
    for i in range(num_split_AD + 2):
        for j in range(num_split_AB + 2):
            x = points_coordinate_AB[j][0] + (points_coordinate_DC[j][0] - points_coordinate_AB[j][0]) / (
                    num_split_AD + 1) * (i + 1)
            y = points_coordinate_AB[j][1] + (points_coordinate_DC[j][1] - points_coordinate_AB[j][1]) / (
                    num_split_AD + 1) * (i + 1)
            points_coordinate_result.append([x, y])
            strtt = strtt + str(x) + "," + str(y) + ";"

    points_coordinate_result.extend(points_coordinate_AB)
    points_coordinate_result.extend(points_coordinate_DC)

    print(len(points_coordinate_result))

    return points_coordinate_result
'''
print('======================================')
print(points_coordinate_result)
print('字符串：'+ strtt.strip(";"))
'''

'''
latA = 116.371067
lonA = 39.959193
latB = 116.483032
lonB = 39.973018

d2 = get_distance(lonA, latA, lonB, latB)
print(d2)  #9.664978035037414
'''

def create_yichuxing_data(points_coordinate_result):
    '''生成宜出行爬取的数据各式'''
    text = 'OBJECTID,x,y\n'
    for i, point in enumerate(points_coordinate_result):
        lng = points_coordinate_result[i][0]
        lat = points_coordinate_result[i][1]
        '''
        res = transCoordinateSystem.bd09_to_wgs84(lng, lat)
        lng = res[0]
        lat = res[1]
        '''
        text += str(i) + ',' + str(lng) + ',' + str(lat) + '\n'

    path = "/static/blog/file/" + str(uuid.uuid4()).replace("-", "") + '.txt'
    with open(os.getcwd() + "/apps/blog" + path, 'w') as f:
        f.write(text.strip())
    print('写入成功')
    return path

def get_grid_data():
    points_coordinate_result = get_ss()
    create_yichuxing_data(points_coordinate_result)


'''
point_A = 117.06, 39.2  # 左上角点，x619
point_D = 117.06, 39.03  # 左下角点，农场十一队
point_B = 117.33, 39.2  # 右上角点，木妙
point_C = 117.33, 39.03  # 右下角点，牛场右下角
require_distance = 2.6
points = get_ss(point_A, point_D, point_B, point_C, require_distance)

print(len(points))
'''
