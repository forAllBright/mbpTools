# -*- coding: utf-8 -*-
# @Author: pmz
# @Date:   2018-12-23 20:58:29
# @Last Modified by:   pmz
# @Last Modified time: 2019-01-03 10:14:48
# TODO: 后续增加 seu status 命令,用来显示登录或登的状态,不做登录或登出动作.

import urllib
from workflow import Workflow
import requests
import sys
import json
import socket
import time
import datetime
import ssl

reload(sys)
sys.setdefaultencoding('utf8')

ICON_DEFAULT = 'FLOW_ICON.png'
ICON_LOGIN = 'ICON_LOGIN.png'
ICON_IP = 'ICON_IP.png'
ICON_ERROR = 'ICON_ERROR.png'


def get_set_lastlogin_timer(update_in=False, update_out=False):
    data = ''
    with open('timer.json', 'r') as f:
        data = json.loads(f.read())
    last_login_time = int(data['last_login_time'])
    last_logout_time = int(data['last_logout_time'])
    if update_in:
        data['last_login_time'] = int(time.time())
        with open('timer.json', 'w') as f:
            json.dump(data, f)
    if update_out:
        data['last_logout_time'] = int(time.time())
        with open('timer.json', 'w') as f:
            json.dump(data, f)
    return {
        'last_login_time': last_login_time,
        'last_logout_time': last_logout_time
    }


def post_web_data(url, username, password):
    auth = {"username": username, "password": password}
    headers = {
        "User-Agent":
        r"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }
    resp = requests.post(url=url, params=auth, headers=headers, verify=False).json()
    return resp

def get_web_data(url):
    headers = {
        "User-Agent":
        r"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }
    resp = requests.get(url=url, headers=headers, verify=False).json()
    return resp


def is_connected(hostname="www.baidu.com"):
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(hostname)
        # connect to the host -- tells us if the host is actually
        # reachable
        s = socket.create_connection((host, 80), 2)

        # CREATE SOCKET
        # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # sock.settimeout(2)
        # wrappedSocket = ssl.wrap_socket(sock)
        # # CONNECT AND PRINT REPLY
        # HOST = socket.gethostbyname(hostname)
        # PORT = 80
        # wrappedSocket.connect(('119.75.217.109', 80))
        # wrappedSocket.close()
        return True
    except:
        pass
    return False


def main(wf):
    url = sys.argv[sys.argv.index('-url') + 1] if '-url' in sys.argv else None
    url_ip = socket.gethostbyname(url)
    username = ''
    password = ''
    query = str(wf.args[0]).strip()
    if not query:
        wf.add_item('seu-wlan login')
        wf.send_feedback()
        return 0

    if wf.args[0].strip() in ["login", "li"]:
        url = "http://{}/index.php/index/login".format(url_ip)
        username = sys.argv[sys.argv.index('-username') +
                            1] if '-username' in sys.argv else None
        password = sys.argv[sys.argv.index('-password') +
                            1] if '-password' in sys.argv else None
        resp = post_web_data(url, username, password)
    elif wf.args[0].strip() in ["logout", "lo"]:
        url = "http://{}/index.php/index/logout".format(url_ip)
        resp = post_web_data(url, username, password)
    elif wf.args[0].strip() in ["status", "st"]:
        url = "http://{}/index.php/index/init".format(url_ip)
        resp = get_web_data(url)
    else:
        pass
    decode_info = resp['info'].decode('utf-8')

    update_in = False
    update_out = False
    if decode_info == "用户已登录":
        update_in = False
        status = True
        print "用户已登录"
    elif decode_info == "认证成功":
        update_in = True
        print "认证成功"
    elif decode_info == "用户已退出":
        update_out = False
        print "用户已注销登录"
    elif decode_info == "退出成功":
        update_out = True
        print "用户注销登录成功"
    elif decode_info == "用户未登录":
        status = False
        print "用户未登录"
    else:
        print decode_info
        if is_connected():
            print "😀 外网访问正常"
        else:
            print "😥 不能访问外部网络"
        return 0

    # if 'logout_ip' in resp:
    #     print "上次登录IP: {}\n".format(resp['logout_ip'])
    # else:
    #     pass
    if wf.args[0].strip() in ["login", "li"]:
        get_set_lastlogin_timer(update_in=update_in)
        lin_lout = get_set_lastlogin_timer(update_in=update_in)
        lin = lin_lout['last_login_time']
        lout = lin_lout['last_logout_time']
        print "通过wf登录时间: {}".format(datetime.datetime.fromtimestamp(lin))
    elif wf.args[0].strip() in ["logout", "lo"]:
        if update_out:
            url_tmp = "http://{}/index.php/index/init".format(url_ip)
            # resp = requests.get(url_tmp).json()
            # print "本次在线时间: {}".format(datetime.timedelta(seconds=resp['logout_timer']))
        else:
            lin_lout = get_set_lastlogin_timer(update_out=False)
            lin = lin_lout['last_login_time']
            lout = lin_lout['last_logout_time']
            print "上次通过wf登出时间: {}".format(datetime.datetime.fromtimestamp(lout))
    else:
        if status:
            print "在线时长: {}".format(
                datetime.timedelta(seconds=resp['logout_timer']))
        else:
            lin_lout = get_set_lastlogin_timer(update_in=update_in)
            lin = lin_lout['last_login_time']
            lout = lin_lout['last_logout_time']
            print "上次通过wf登录时间: {}".format(datetime.datetime.fromtimestamp(lin))


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
