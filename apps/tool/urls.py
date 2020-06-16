# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import (Toolview, BD_pushview, bd_api_view, BD_pushview_site, bd_api_site, Link_testview,
                    Link_test_api, regexview, regex_api, useragent_view, useragent_api, html_characters,
                    tencentview, tencent_data, poi_view, poi_data, getSubdistrict, poi_visual, upload,heatmap_visual

        , coord_view, poicoordtransform, coordpick, yichuxing_view, yichuxing_data, polygon_view, poi_polygon_data
        , gridview, grid_generate, boundaryview, boundarydata, common_file_upload, common_file_download, common_file_download_coord,
                    bmappoi, bmappoidata, common_file_download_yichuxing_chengdu)

urlpatterns = [
    url(r'^$', Toolview, name='total'),  # 工具汇总页
    url(r'^baidu-linksubmit/$', BD_pushview, name='baidu_push'),  # 百度主动推送
    url(r'^baidu-linksubmit/ajax/$', bd_api_view, name='baidu_push_api'),  # 百度推送ajax
    url(r'^baidu-linksubmit-for-sitemap/$', BD_pushview_site, name='baidu_push_site'),  # 百度主动推送sitemap
    url(r'^baidu-linksubmit-for-sitemap/ajax/$', bd_api_site, name='baidu_push_api_site'),
    url(r'^link-test/$', Link_testview, name='link_test'),  # 友链检测
    url(r'^link-test/ajax/$', Link_test_api, name='link_test_api'),
    url(r'^regex/$', regexview, name='regex'),  # 正则表达式在线
    url(r'^regex/ajax/$', regex_api, name='regex_api'),
    url(r'^user-agent/$', useragent_view, name='useragent'),  # user-agent生成器
    url(r'^user-agent/ajax/$', useragent_api, name='useragent_api'),
    url(r'^html-special-characters/$', html_characters, name='html_characters'),  # HTML特殊字符查询
    url(r'^tencet/$', tencentview, name='tencent'),  # 腾讯位置大数据爬取页面
    url(r'^tencentdata/$', tencent_data, name='tencent_data'),  # 腾讯位置大数据爬取
    url(r'^poiview/$', poi_view, name='poi_view'),  # POI数据爬取页面
    url(r'^poidata/$', poi_data, name='poi_data'),  # POI数据爬取
    url(r'^subdistrictdata/$', getSubdistrict, name='subdistrict_data'),  # P获取行政区数据
    url(r'^poi_visual/$', poi_visual, name='poi_visual'),  # P获取行政区数据
    url(r'^upload/$', upload, name='upload'),  # P获取行政区数据
    url(r'^heatmap_visual/$', heatmap_visual, name='heatmap_visual'),  # 热力图可视化页面
    url(r'^coord_view/$', coord_view, name='coord_view'),  # 坐标转换页面
    url(r'^poicoordtransform/$', poicoordtransform, name='poicoordtransform'),  # 坐标转换
    url(r'^coordpick/$', coordpick, name='coordpick'),  # 坐标拾取页面
    url(r'^yichuxing_view/$', yichuxing_view, name='yichuxing'),  # 宜出行数据爬取页面
    url(r'^yichuxing_data/$', yichuxing_data, name='yichuxing_data'),  # 宜出行数据爬取
    url(r'^polygon_view/$', polygon_view, name='polygon_view'),  # 矩形范围爬取POI页面
    url(r'^poi_polygon_data/$', poi_polygon_data, name='poi_polygon_data'),  # 矩形范围爬取POI
    url(r'^gridview/$', gridview, name='gridview'),  # 矩形网格生成页面
    url(r'^grid_generate/$', grid_generate, name='grid_generate'),  # 矩形网格生成
    url(r'^boundaryview/$', boundaryview, name='boundaryview'),  # 矩形网格生成页面
    url(r'^boundarydata/$', boundarydata, name='boundarydata'),  # 矩形网格生成
    url(r'^common_file_upload/$', common_file_upload, name='common_file_upload'),  # 文件上传
    url(r'^common_file_download/$', common_file_download, name='common_file_download'),  # 文件下载
    url(r'^common_file_download_coord/$', common_file_download_coord, name='common_file_download_coord'),  # 文件下载
    url(r'^bmappoi/$', bmappoi, name='bmappoi'),  # 百度地图POI数据采集
    url(r'^bmappoidata/$', bmappoidata, name='bmappoidata'),  # 百度地图POI数据采集
    url(r'^common_file_download_yichuxing_chengdu/$', common_file_download_yichuxing_chengdu, name='common_file_download_yichuxing_chengdu'),  # 百度地图POI数据采集



]
