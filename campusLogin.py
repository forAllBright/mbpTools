#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: forAllBright
# @Date:   2018-12-22 17:58:16
# @Last Modified by:   forAllBright
# @Last Modified time: 2019-03-13 16:40:54
########################################################
# 用来配合 Alfred 快速认证登录校园网
########################################################

import requests
from bs4 import BeautifulSoup
import socket
import sys
import json
import argparse

parser = argparse.ArgumentParser(
    description="seu campus wlan login command line tool")
parser.add_argument(
    "-l", "--log", required=True, help="option login or logout")
args = parser.parse_args()


class bcolors:
    # Colors
    PURPLE = '\033[1;35;1m'
    RED = '\033[1;31;1m'
    BLUE = '\033[1;34;1m'
    GREEN = '\033[1;32;1m'
    CYAN = "\033[1;36;1m"
    YELLOW = "\033[1;33;1m"
    BLACK = "\033[1;30;1m"
    WHITE = "\033[1;37;1m"
    # Font effects
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    NEFATIVE1 = '\033[3m'
    NEFATIVE2 = '\033[5m'
    # Background colors
    BACKGROUND_BLACK = "\033[;;40m"
    BACKGROUND_RED = "\033[;;41m"
    BACKGROUND_GREEN = "\033[;;42m"
    BACKGROUND_YELLOW = "\033[;;43m"
    BACKGROUND_BLUE = "\033[;;44m"
    BACKGROUND_PURPLE = "\033[;;45m"
    BACKGROUND_CYAN = "\033[;;46m"
    BACKGROUND_WHITE = "\033[;;47m"


def login_request(login_url, username, password):
    response = requests.post(
        login_url,  # URL
        {
            'username': username,
            'password': password,
        },  # form-data
        headers={
            "User-Agent":
            r"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        },  # headers
        verify=False  # this simply disables SSL security check
    )
    root = BeautifulSoup(response.content, "html.parser")
    return root  # dict


def pre_login(main_url):
    try:
        socket.create_connection((main_url, 80), 2)
    except socket.error:
        print("{} connect error")
        sys.exit(1)
    try:
        main_ip = socket.gethostbyname(main_url)
    except socket.error:
        print("{} ip parse error")
        sys.exit(1)
    return main_ip


def parse_response(resp):
    resp_str = str(resp)
    resp_json = json.loads(resp_str)
    info, status = resp_json['info'], resp_json['status']
    return (info, status)


if __name__ == "__main__":
    main_url = "w.seu.edu.cn"
    username = "你的账号"
    password = "base64加密后你的密码"
    main_ip = pre_login(main_url)
    resp = ''
    if args.log == 'login':
        resp = login_request("http://{}/index.php/index/login".format(main_ip),
                             username, password)
    elif args.log == 'logout':
        resp = login_request("http://{}/index.php/index/logout".format(main_ip),
                     '', '')
    info, status = parse_response(resp)
    if status == 1 and args.log == 'login':
        print(bcolors.GREEN + " **** " + info + " **** " + bcolors.ENDC)
        print(bcolors.GREEN + "Login IP: {}".format(json.loads(str(resp))['logout_ip']) + bcolors.ENDC)
    elif status == 1 and args.log == 'logout':
        print(bcolors.GREEN + " **** " + info + " **** " + bcolors.ENDC)
    elif status == 0:
        print(bcolors.RED + info + bcolors.ENDC)
