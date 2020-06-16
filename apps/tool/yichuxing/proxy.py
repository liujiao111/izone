import requests
import json
import apps.tool.yichuxing.settings as settings
import time

count = 0
def getproxy():
    xdaili_order_id = settings.xdaili_order_id
    xdaili_spiderId = settings.xdaili_spiderId
    print(xdaili_order_id, xdaili_spiderId)
    url = 'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=' + xdaili_spiderId + '&orderno=' + xdaili_order_id + '&returnType=2&count=1'
    data = requests.get(url)    #'{"ERRORCODE":"0","RESULT":[{"port":"29377","ip":"117.69.200.128"}]}'
    data = json.loads(data.text)
    if data['ERRORCODE'] == "0":
        return data['RESULT'][0]['ip'], data['RESULT'][0]['port']
    print("============代理获取失败，详细信息：" + json.dumps(data))
    if data['ERRORCODE'] == "10032":
        return None, '今日提取已达上限，请隔日提取或额外购买'

    if data['ERRORCODE'] == "10036" or data['ERRORCODE'] == "10038" or data['ERRORCODE'] == "10055":
        print('提取过快')
        time.sleep(5)
        return getproxy()
