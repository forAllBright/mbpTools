#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: pmz
# @Date:   2018-12-23 20:58:29
# @Last Modified by:   pmz
# @Last Modified time: 2019-01-03 10:04:19

import json
import time
import datetime
import requests

# data = ''
# with open('timer.json','r') as f:
#     data = json.loads(f.read())
#     print(data)
#     print(type(data['last_login_time']))
#     data['last_login_time'] = time.time()
# with open('timer.json', 'w') as f:
#         json.dump(data, f)


# def get_set_lastlogin_timer(update_in=False, update_out=False):
#     data = ''
#     with open('timer.json', 'r') as f:
#         data = json.loads(f.read())
#     last_login_time = int(data['last_login_time'])
#     last_logout_time = int(data['last_logout_time'])
#     if update_in:
#         data['last_login_time'] = int(time.time())
#         with open('timer.json', 'w') as f:
#             json.dump(data, f)
#     if update_out:
#         data['last_logout_time'] = int(time.time())
#         with open('timer.json', 'w') as f:
#             json.dump(data, f)
#     return {
#         'last_login_time': last_login_time,
#         'last_logout_time': last_logout_time
#     }
# update_in = True

# lin_lout = get_set_lastlogin_timer(update_in=update_in)
# lin = lin_lout['last_login_time']
# lout = lin_lout['last_logout_time']
# print("登录时间: {}".format(datetime.datetime.fromtimestamp(lin)))

url_tmp = "https://121.248.62.222/index.php/index/init"
resp = requests.get(url_tmp,verify=False).json()
print(resp)
print("本次在线时间: {}".format(datetime.timedelta(seconds=resp['logout_timer'])))