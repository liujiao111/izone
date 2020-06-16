
## 使用说明

## 使用前配置
所有需要修改的配置都在settting.py文件中，以TODO样式标出，有四个地方需要修改

## 确定爬取经纬度范围
坐标拾取系统拾取需要爬取的城市四个角的坐标，地址：http://www.mapboxx.cn/tool/coordpick/，分别填入setting.py的

```
# 需要爬取的城市四个角的经纬度
city_bound_point_A=103.828027,30.84057#左上角点，x619
city_bound_point_D=103.627956,30.243391 #左下角点，农场十一队
city_bound_point_B=104.724895,30.802859 #右上角点，木妙
city_bound_point_C=104.876673,30.259364 #右下角点，牛场右下角
```

替换等号后面的值

## 登录qq获取cookie
分别登录多个qq,打开邮箱或者空间，然后打开宜出行官网，地址：https://c.easygo.qq.com/eg_toc/map.html?origin=csfw&cityid=110000，打开F12,点击network，查看某个请求的内容，复制cookie值到settings.py中，
```

cookie = ["pgv_pvi=9644207104; RK=oNqVOx31eL; ptcz=376ec54db1b3b1028408b45ac2191b22ccbe534c8d4d5fddd869ced28ded3474; pgv_pvid=2828356968; o_cookie=917961898; tvfe_boss_uuid=78c2e9739b026909; has_show_ilike=1; pac_uid=1_917961898; eas_sid=h1V545k7S7g3X5p772M4Q9Z7i6; ied_qq=o0917961898; qb_qua=; qb_guid=81d9f482dfe24e04924cecc4c301f466; Q-H5-GUID=81d9f482dfe24e04924cecc4c301f466; NetType=; psrf_qqaccess_token=9C89E0B205B72342F77C98CFDC6451AC; psrf_access_token_expiresAt=1574428332; psrf_qqrefresh_token=DB476F5F57061DBB096A26047D598C1C; psrf_qqunionid=F298CACC345166E0DD7EF1F51169B15A; qm_keyst=Q_H_L_2mwDXr50eeAhlSQj1SO_nqyIMCCF4ZP6lSfZPJ6csK8tAHPg-PT2ta2nHK1Gjz5; psrf_musickey_createtime=1566652332; psrf_qqopenid=7E05A9D1A94CAAF9C327F71FEA3E5631; ptui_loginuin=917961898; php_session=eyJpdiI6IlMraHBseVZTUDY1Z0FuRHp3SXhkNmc9PSIsInZhbHVlIjoiejdoRE1YbGJCMkdqdlo2bjNsVGJEY3R3SG5nUEVXeTRaN3VlRlA2cVZpb1ZTQThWaGZna0p5QlRcLzV1ZVJodzZiSFo2V2pTd0RTZW1RNnBWNU9HMlJBPT0iLCJtYWMiOiIxMjhkMTJjODFhMWRhODRiNmNjODMyMDc0OTE1NjFmZjdlMzQ1ODVlYzczMTc1NmI3YmQ2YWQzMzQyNjZiMDE4In0%3D; uin=o2242382677; skey=@E4lp4zTwC; ptisp=ctc; pgv_info=ssid=s754459976"

]
```

多个格式的话照此格式填写即可，为了避免出现出现明天再来吧的提示，尽量多登录几个qq填写

## 申请代理
讯代理下单，然后填代理的spiderId和secret，例如：

```
xdaili_spiderId="rbrhrfb45453"
xdaili_order_id="3g4hy46434"
```

## 运行程序
- 执行main.py文件或者run.bat。完成后会在当前目录的example目录下生成.csv文件。
- 打开热力图可视化工具，地址：http://www.mapboxx.cn/tool/heatmap_visual/，上传刚刚的csv文件，即可看到可视化的数据。

## 注意
- 爬取范围最好不要太大
- 每次爬取前最好切换cookie，否则会导致单个qq号爬取太多数据被封的情况，如果控制台出现错误，重新登录个qq获取cookie再跑一次就好啦
