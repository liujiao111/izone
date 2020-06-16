#! /usr/local/bin/python3
# coding: utf-8
# __author__ = "Brady Hu"
# __date__ = 2017/10/16 16:11

import os

#爬虫参数设置

xy_name = "data.txt"

#下面设置文件存目录，不要设置在系统盘，不然会出现问题
#当前目录用"."表示，如"./example/"
filepath = r"./example/"
if not os.path.exists(filepath):
	os.makedirs(filepath)
filename = "example"


cookies = []



xdaili_order_id = 'YZ20198317551IEhRPV'
xdaili_spiderId = '8b00f6694df8471f87f8961bc0c3e9a6'