#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re
import socket

try:
    resp = requests.get(
        ur"https://www.ipchicken.com/",
        headers={
            u"User-Agent":
            ur"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        },  # headers
        verify=True)
    data = BeautifulSoup(resp.text, u"html.parser")
    # pprint(data.find_all(face="Verdana, Arial, Helvetica, sans-serif", size="5"))
    ip_html =data.find_all(face=u"Verdana, Arial, Helvetica, sans-serif", size=u"5")
    ip_tag = ip_html[0]
    ip_str = unicode(ip_tag)
    ip = u''
    o_ip_tmp = re.search(ur'(\d+\.)+\d+',ip_str)
    o_ip = o_ip_tmp.group(0)
    print u"Outside address: {}".format(o_ip)
except:
    print u"WWAN Offline"

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    s.connect((u"8.8.8.8", 80))
    i_ip = s.getsockname()[0]
    if not i_ip == u'0.0.0.0':
        print u"LAN address: {}".format(i_ip)
    else:
        print u"LAN Offline"
except:
    print u"LAN Offline"
s.close()