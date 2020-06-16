from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.utils.html import mark_safe
from .apis.bd_push import push_urls, get_urls
from .apis.links_test import Check
from .apis.useragent import get_user_agent
from django.http import FileResponse
import re
import markdown

from django.shortcuts import render

import os
import json
import time
import apps.tool.tencendata as tdata
import apps.tool.poi as poi
import apps.tool.poi_polygon as poi_polygon
import apps.tool.heatmap  as heatmap
import apps.tool.coord  as coord
import apps.tool.get_grid as get_grid
from apps.tool.yichuxing import settings, main
from apps.tool.boundary import get_boundary, parse_boundary
from apps.tool.bmappoidata import get_bmap_data
import apps.tool.config as config

FILE_DOWNLOAD_FOLDER = os.getcwd() + os.sep + "apps" + os.sep + "blog" + os.sep + "static" + os.sep + "blog" + os.sep + "commonfile" + os.sep


@require_POST
def common_file_upload(request):
    '''
        公共的文件上传
    '''
    if request.method == "POST":  # 请求方法为POST时，进行处理
        myFile = request.FILES.get("myfile", None)  # 获取上传的文件，如果没有文件，则默认为None
        file_path = os.getcwd() + "/data/upload/" + myFile.name
        if not myFile:
            return JsonResponse(json.loads({"message": "File is None"}))
        destination = open(os.path.join(os.getcwd() + "/data/upload", myFile.name), 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        text = '''{"file_path": "''' + file_path.replace("\\", "\\\\") + '''", "status":"200"}'''
        return JsonResponse(json.loads(text))


def common_file_download(request):
    '''
        公共的文件下载
    '''
    # filename = request.GET['filename']
    filename = " "
    if filename == None or filename == " ":
        filename = 'bmap-poi-boundaey-templete.csv'
    file_full_name = FILE_DOWNLOAD_FOLDER + filename
    print('文件存放地址：', file_full_name)
    file = open(file_full_name, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=' + file_full_name.split(os.sep)[
        len(file_full_name.split(os.sep)) - 1] + ''
    return response


def common_file_download_coord(request):
    '''
        坐标转换模板文件下载
    '''

    filename = " "
    if filename == None or filename == " ":
        filename = 'coord-transform-template.xls'
    file_full_name = FILE_DOWNLOAD_FOLDER + filename
    file = open(file_full_name, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=' + file_full_name.split(os.sep)[
        len(file_full_name.split(os.sep)) - 1] + ''
    return response


def common_file_download_yichuxing_gugong(request):
    '''
        宜出行热力数据模板下载-故宫
    '''

    filename = " "
    if filename == None or filename == " ":
        filename = 'heatdata--gugong-2019-11-29-10-13-36.csv'
    file_full_name = FILE_DOWNLOAD_FOLDER + filename
    file = open(file_full_name, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=' + file_full_name.split(os.sep)[
        len(file_full_name.split(os.sep)) - 1] + ''
    return response



def common_file_download_yichuxing_chengdu(request):
    '''
        宜出行热力数据模板下载-成都
    '''

    filename = " "
    if filename == None or filename == " ":
        filename = 'heatdata--gugong-2019-11-29-10-13-36.csv'
    file_full_name = FILE_DOWNLOAD_FOLDER + filename
    file = open(file_full_name, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=' + file_full_name.split(os.sep)[
        len(file_full_name.split(os.sep)) - 1] + ''
    return response



# Create your views here.

def Toolview(request):
    return render(request, 'tool/tool.html')


# 百度主动推送
def BD_pushview(request):
    return render(request, 'tool/bd_push.html')


@require_POST
def bd_api_view(request):
    if request.is_ajax():
        data = request.POST
        url = data.get('url')
        urls = data.get('url_list')
        info = push_urls(url, urls)
        return JsonResponse({'msg': info})
    return JsonResponse({'msg': 'miss'})


# 百度主动推送升级版，提取sitemap链接推送
def BD_pushview_site(request):
    return render(request, 'tool/bd_push_site.html')


@require_POST
def bd_api_site(request):
    if request.is_ajax():
        data = request.POST
        url = data.get('url')
        map_url = data.get('map_url')
        urls = get_urls(map_url)
        if urls == 'miss':
            info = "{'error':404,'message':'sitemap地址请求超时，请检查链接地址！'}"
        elif urls == '':
            info = "{'error':400,'message':'sitemap页面没有提取到有效链接，sitemap格式不规范。'}"
        else:
            info = push_urls(url, urls)
        return JsonResponse({'msg': info})
    return JsonResponse({'msg': 'miss'})


# 友链检测
def Link_testview(request):
    return render(request, 'tool/link_test.html')


@require_POST
def Link_test_api(request):
    if request.is_ajax():
        data = request.POST
        p = data.get('p')
        urls = data.get('urls')
        c = Check(urls, p)
        info = c.run()
        return JsonResponse(info)
    return JsonResponse({'msg': 'miss'})


# 在线正则表达式
def regexview(request):
    return render(request, 'tool/regex.html')


@require_POST
def regex_api(request):
    if request.is_ajax():
        data = request.POST
        texts = data.get('texts')
        regex = data.get('r')
        try:
            lis = re.findall(r'{}'.format(regex), texts)
        except:
            lis = []
        num = len(lis)
        info = '\n'.join(lis)
        result = "匹配到&nbsp;{}&nbsp;个结果：\n".format(num) + "```\n" + info + "\n```"
        result = markdown.markdown(result, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        return JsonResponse({'result': mark_safe(result), 'num': num})
    return JsonResponse({'msg': 'miss'})


# 生成请求头
def useragent_view(request):
    return render(request, 'tool/useragent.html')


@require_POST
def useragent_api(request):
    if request.is_ajax():
        data = request.POST
        d_lis = data.get('d_lis')
        os_lis = data.get('os_lis')
        n_lis = data.get('n_lis')
        d = d_lis.split(',') if len(d_lis) > 0 else None
        os = os_lis.split(',') if len(os_lis) > 0 else None
        n = n_lis.split(',') if len(n_lis) > 0 else None
        result = get_user_agent(os=os, navigator=n, device_type=d)
        return JsonResponse({'result': result})
    return JsonResponse({'msg': 'miss'})


# HTML特殊字符对照表
def html_characters(request):
    return render(request, 'tool/characters.html')


# 腾讯位置大数据爬取-页面
def tencentview(request):
    return render(request, 'tool/tencent.html')


# 腾讯位置大数据爬取
def tencent_data(request):
    max_lon = request.GET['max_lon']
    min_lon = request.GET['min_lon']
    max_lat = request.GET['max_lat']
    min_lat = request.GET['min_lat']

    if len(max_lon) > 5:
        max_lon = max_lon[0:5]
    if len(min_lon) > 5:
        min_lon = min_lon[0:5]

    if len(max_lat) > 4:
        max_lat = max_lat[0:4]
    if len(min_lat) > 4:
        min_lat = min_lat[0:4]

    if (max_lon is None or max_lon is ''):
        return render(request, 'tool/tencent.html', {'message': '请输入完整的范围经纬度!'})
    if (min_lon is None or max_lon is ''):
        return render(request, 'tool/tencent.html', {'message': '请输入完整的范围经纬度!'})
    if (max_lat is None or max_lon is ''):
        return render(request, 'tool/tencent.html', {'message': '请输入完整的范围经纬度!'})
    if (min_lat is None or max_lon is ''):
        return render(request, 'tool/tencent.html', {'message': '请输入完整的范围经纬度!'})

    try:
        max_lon = int(max_lon)
        min_lon = int(min_lon)
        max_lat = int(max_lat)
        min_lat = int(min_lat)
    except Exception as e:
        return render(request, 'tool/tencent.html', {'message': '请输入整数类型的经纬度'})

    tdata.max_lon_default = max_lon
    tdata.min_lon_default = min_lon
    tdata.max_lat_default = max_lat
    tdata.min_lat_default = min_lat

    flag = True
    now_time_str = str(time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time())))
    file_name = "TecentData-" + now_time_str + ".csv"
    while (flag):
        for i in range(4):
            try:
                tdata.get_TecentData(4, i, file_name)  # 主要是循环count，来获取四个链接里的数据
            except Exception as e:
                return render(request, 'tencent.html', {'message': '爬取失败，请联系管理员'})
        flag = False

        file_path = os.getcwd() + "/" + file_name

        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename=' + file_name + ''
        return response


def poi_view(request):
    return render(request, 'tool/poi.html')


@require_POST
def poi_data(request):
    '''
    根据关键字爬取POI数据
    :param request:
    :return:
    '''

    data = request.POST
    city = data.get('city')
    province = data.get('province')
    keyword = data.get('keyword')
    key = data.get('key')  # "4188efb67360681f89110ccdb11e563b"
    coord = data.get('coord')

    # TODO:
    # province = "500000"
    # keyword = "大学"
    # key = "9f27cbb8d65567505df8cae9dac49aa3"

    if (province == None or province == ""):
        return render(request, 'tool/poi.html', {'message': "城市或直辖市不能为空"})
    if (keyword == None or keyword == ""):
        return render(request, 'tool/poi.html', {'message': "POI关键字不能为空"})
    #    if (key == None or key == ""):
    # return render(request, 'tool/poi.html',  {'message':"密钥不能为空，如有需要请自行申请或者联系917961898获取"})

    print('提交参数：', province, city, keyword, coord, key)

    try:
        filename = poi.get_data(province, city, keyword, coord, key)
    except Exception as e:
        message = "爬取失败" + str(e)
        return render(request, 'tool/poi.html', {'message': message})
    if filename == None:
        return render(request, 'tool/poi.html', {'message': "爬取失败"})

    file_path = os.getcwd() + "/" + filename

    file = open(file_path, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=' + filename + ''
    return response


# getSubdistrict
def getSubdistrict(request):
    '''
    根据省编号获取城市数据
    :return:
    '''
    code = request.GET['code']
    print(code)
    data = poi.get_distrinct(code)
    return JsonResponse(json.loads(data))


def poi_visual(request):
    return render(request, 'tool/poivisual.html')


def heatmap_visual(request):
    return render(request, 'tool/heatmapvisual.html')


UPLOAD_FOLDER = '/upload'

ALLOWED_EXTENSIONS = set(['csv', 'xls', 'xlsx', 'txt'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@require_POST
def upload(request):
    '''
    文件上传
    TODO
    :return:
    '''

    if request.method == "POST":  # 请求方法为POST时，进行处理
        myFile = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None
        file_path = os.getcwd() + "/data/upload/" + myFile.name
        if not myFile:
            return JsonResponse(json.loads({"message": "File is None"}))
        destination = open(os.path.join(os.getcwd() + "/data/upload", myFile.name), 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()

        # 将EXCEL数据处理为百度地图可视化展示需要的格式
        data = request.POST
        type = data.get('type')
        if type == "poi":
            data = poi.get_poi_map_data(file_path)
        elif type == "heatmap":
            # 热力图
            data = heatmap.get_map_data(file_path)
        elif type == "coord":
            # 坐标转换
            data = {"filename": file_path}

        return JsonResponse(data, safe=False)


def coord_view(request):
    return render(request, 'tool/coord.html')


@require_POST
def poicoordtransform(request):
    '''
    坐标转换
    :param request:
    :return:
    '''
    data = request.POST
    orgcoord = data.get('orgcoord')
    targetcoord = data.get('targetcoord')
    filename = data.get('filename')

    download_file_name = 'result.xls'
    if orgcoord == None or orgcoord == " " or targetcoord == None or targetcoord == " ":
        return render(request, 'tool/coord.html', {'message': '请选择需要转换的坐标！'})

    if filename == None or filename == " ":
        return render(request, 'tool/coord.html', {'message': '请上传文件后再操作！'})

    sub_fix = str(filename).split(".")[-1].split()[0]

    try:
        if sub_fix == 'xls':
            new_file_name = coord.transfer(orgcoord, targetcoord, filename)
        elif sub_fix == 'csv':
            new_file_name = coord.transfer_csv(orgcoord, targetcoord, filename)
            download_file_name = 'result.csv'
        else:
            return render(request, 'tool/coord.html', {'message': '暂不支持！' + sub_fix + "格式的数据"})
    except Exception as e:
        return render(request, 'tool/coord.html', {'message': '坐标转换失败：' + str(e)})
    print('转换后的EXCEL地址：', new_file_name)

    file = open(new_file_name, 'rb')
    #filename = , #new_file_name.split(os.sep)[len(new_file_name.split(os.sep))-1] + ''

    print('下载文件名：', filename)

    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=' + download_file_name + ''
    return response


def yichuxing_view(request):
    '''
    宜出行人流量爬取页面
    :param request:
    :return:
    '''
    return render(request, 'tool/yichuxing.html')


def yichuxing_data(request):
    '''
        宜出行人流量爬取
        :param request:
        :return:
        '''

    ycx_points = request.GET['ycx_points']
    ycx_cookie = request.GET['ycx_cookie']
    userKey = request.GET['userKey']

    max_lon = request.GET['max_lon']
    min_lon = request.GET['min_lon']
    max_lat = request.GET['max_lat']
    min_lat = request.GET['min_lat']

    if userKey != "HGKRT4MD32MS2K32" and userKey != 'ASDJRKDJER854J2J4J36':
        return render(request, 'tool/yichuxing.html', {'message': '密钥不正确，请联系：917961898!'})

    # if len(str(ycx_points).split(";")) > 50:
    # return render(request, 'tool/yichuxing.html', {'message': '网格点太多，请保持在50个以下'})

    if userKey == 'ASDJRKDJER854J2J4J36':
        if len(str(ycx_points).split(";")) > 2:
            return render(request, 'tool/yichuxing.html', {'message': '网格点太多!，最多只能两个'})
    '''
        for one_cookie in str(ycx_cookie).split("||"):
        if one_cookie != None and one_cookie != "":
            settings.cookies.append(one_cookie)
            '''

    # 遍历网格，爬取数据，汇总后去重写入CSV中

    result_file_name, code = main.get_data(ycx_points, ycx_cookie, max_lon, min_lon, max_lat, min_lat)
    if code == 500:
        return render(request, 'tool/yichuxing.html', {'message': '爬取失败，详细信息：' + result_file_name})

    file = open(result_file_name, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=' + result_file_name.split("/")[
        len(result_file_name.split("/")) - 1] + ''
    return response


def coordpick(request):
    '''
    坐标拾取页面
    :return: coordpick.html
    '''
    return render(request, 'tool/coordpick.html')


def polygon_view(request):
    '''
     矩形范围爬取POI页面
    :param request:
    :return:
    '''
    return render(request, 'tool/polygon.html')


@require_POST
def poi_polygon_data(request):
    '''
    根据矩形范围爬取POI数据
    :param request:
    :return:
    '''

    data = request.POST
    city = data.get('city')
    province = data.get('province')
    keyword = data.get('keyword')
    key = data.get('key')  # "4188efb67360681f89110ccdb11e563b"
    coord = data.get('coord')

    # TODO:
    # province = "500000"
    # keyword = "大学"
    # key = "9f27cbb8d65567505df8cae9dac49aa3"

    if (province == None or province == ""):
        return render(request, 'tool/poi.html', {'message': "城市或直辖市不能为空"})
    if (keyword == None or keyword == ""):
        return render(request, 'tool/poi.html', {'message': "POI类型不能为空"})
    if (key == None or key == ""):
        return render(request, 'tool/poi.html', {'message': "密钥不能为空，如有需要请自行申请或者联系917961898获取"})

    print('提交参数：', province, city, keyword, coord, key)
    filename = poi_polygon.get_data(province, city, keyword, coord, key)
    if filename == None:
        return render(request, 'tool/poi.html', {'message': "爬取失败"})

    file_path = os.getcwd() + "/" + filename

    file = open(file_path, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=' + filename + ''
    return response


def gridview(request):
    '''
        划分矩形网格页面
        :return:
        '''
    return render(request, 'tool/grid.html')


def grid_generate(request):
    '''
    划分矩形网格
    :return:
    '''
    max_lon = request.GET['max_lon']
    min_lon = request.GET['min_lon']
    max_lat = request.GET['max_lat']
    min_lat = request.GET['min_lat']
    distance = request.GET['distance']

    if (max_lon is None or max_lon is ''):
        return render(request, 'tool/gridview.html', {'message': '请输入完整的范围经纬度!'})
    if (min_lon is None or max_lon is ''):
        return render(request, 'tool/gridview.html', {'message': '请输入完整的范围经纬度!'})
    if (max_lat is None or max_lon is ''):
        return render(request, 'tool/gridview.html', {'message': '请输入完整的范围经纬度!'})
    if (min_lat is None or max_lon is ''):
        return render(request, 'tool/gridview.html', {'message': '请输入完整的范围经纬度!'})

    '''
    max_lon = float(max_lon)
    min_lon = float(min_lon)
    max_lat = float(max_lat)
    min_lat = float(min_lat)
    distance = float(distance)
    '''

    try:

        point_A = float(min_lon), float(max_lat)
        point_D = float(min_lon), float(min_lat)
        point_B = float(max_lon), float(max_lat)
        point_C = float(max_lon), float(min_lat)

        points_coordinate_result = get_grid.get_ss(point_A, point_D, point_B, point_C, float(distance))
        file_path = get_grid.create_yichuxing_data(points_coordinate_result)

        pointsstr = ''
        count = 0
        for point in points_coordinate_result:
            pointsstr += str(point[0]) + "," + str(point[1]) + ";"
            count += 1
        pointsstr = pointsstr.strip(";")
    except Exception as e:
        print('发生异常', e)
        return render(request, 'tool/grid.html', {'message': '服务器异常!'})

    return render(request, 'tool/grid.html',
                  {'message': "网格生成成功", 'count': count, 'points': pointsstr, 'file_path': file_path})


@require_POST
def boundarydata(request):
    '''
   百度多边界边界坐标数据采集
   :param request:
   :return:
   '''

    try:
        data = request.POST
        bmapkey = data.get('bmapkey')
        file_path = data.get('file_path')

        print(bmapkey)
        print(file_path)
        if bmapkey == None or bmapkey == '':
            return render(request, 'tool/boundary.html', {'message': '请输入百度地图密钥!'})
            bmapkey = "1QkdIjutWv0jBDZEKqy9TH4O3divaRcS"

        if file_path == None or file_path == '':
            return render(request, 'tool/boundary.html', {'message': '请上传文件后再操作!'})

        csv_file_path = get_boundary(file_path, bmapkey)

        print('生成的CSV文件地址:', csv_file_path)

        csv_file_path = parse_boundary(csv_file_path)

        print('CSV生成地址：', csv_file_path)
    except Exception as e:
        print('发生异常', e)
        return render(request, 'tool/boundary.html', {'message': '服务器异常!'})

    file = open(csv_file_path, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=' + csv_file_path.split("/")[
        len(csv_file_path.split("/")) - 1] + ''
    return response


# @login_required
def boundaryview(request):
    return render(request, 'tool/boundary.html')


def bmappoi(request):
    '''
    百度POI数据采集页面
    :param request:
    :return:
    '''
    return render(request, 'tool/bmappoi.html')


@require_POST
def bmappoidata(request):
    '''
    百度POI数据采集
    :param request:
    :return:
    '''

    # try:
    data = request.POST

    max_lon = data.get('max_lon')
    min_lon = data.get('min_lon')
    max_lat = data.get('max_lat')
    min_lat = data.get('min_lat')

    keyword = data.get('keyword')
    key = data.get('key')
    coord = data.get('coord')

    if (max_lon == None or max_lon == "" or min_lon == None or min_lon == "" or max_lat == None or max_lat == ""
            or min_lat == None or min_lat == ""):
        return render(request, 'tool/bmappoi.html', {'message': "请输入完整的坐标范围"})
    if (keyword == None or keyword == ""):
        return render(request, 'tool/bmappoi.html', {'message': "POI关键字不能为空"})
    if (key == None or key == ""):
        return render(request, 'tool/bmappoi.html', {'message': "密钥不能为空"})

    print('提交参数：', max_lon, min_lon, max_lat, min_lat, keyword, coord, key)

    # 检查经纬度最大最小是否正确
    max_lon = float(max_lon)
    min_lon = float(min_lon)
    max_lat = float(max_lat)
    min_lat = float(min_lat)

    if max_lon <= min_lon:
        return render(request, 'tool/bmappoi.html', {'message': "最大经度不能小于或等于最小经度"})
    if max_lat <= min_lat:
        return render(request, 'tool/bmappoi.html', {'message': "最大纬度不能小于或等于最小纬度"})

    # 检查需要爬取的范围是否过大
    if max_lon - min_lon > config.bmappoi_max_lon_limit:
        return render(request, 'tool/bmappoi.html',
                      {'message': "范围过大，请保持经度范围在" + str(config.bmappoi_max_lon_limit) + "的范围内"})
    if max_lat - min_lat > config.bmappoi_max_lat_limit:
        return render(request, 'tool/bmappoi.html',
                      {'message': "范围过大，请保持纬度范围在" + str(config.bmappoi_max_lon_limit) + "的范围内"})

    # 开始爬取，并将数据写入EXCEL中，并返回文件路径
    filename = get_bmap_data(max_lon, min_lon, max_lat, min_lat, keyword, coord, key)
    if filename == None:
        return render(request, 'tool/bmappoi.html', {'message': "爬取失败"})

    # 将成功采集到的数据文件提供下载
    file_path = os.getcwd() + "/" + filename
    file = open(file_path, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=' + filename + ''
    return response


'''
    except Exception as e:
    print('百度POI数据采集异常:', e)
    return render(request, 'tool/bmappoi.html', {'message': '服务器异常!'})
    '''
