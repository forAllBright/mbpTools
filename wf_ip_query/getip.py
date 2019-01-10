# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
import requests
from bs4 import BeautifulSoup
import re
import socket
import sys
from workflow import Workflow

reload(sys)
sys.setdefaultencoding('utf8')


def main(wf):
    # LAN IP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect((u"8.8.8.8", 80))
        i_ip = s.getsockname()[0]
        if not i_ip == u'0.0.0.0':
            # print(u"LAN address: {}".format(i_ip))
            wf.add_item(u'LAN IP: {}'.format(i_ip), subtitle='Enter to clipboard', arg=i_ip, valid=True)

        else:
            # print(u"LAN Offline")
            wf.add_item(u'LAN Offline')

    except:
        # print(u"LAN Offline")
        wf.add_item(u'LAN Offline')
    s.close()

    # External IP
    try:
        resp = requests.get(
            "http://ipv4.icanhazip.com",
            headers={
                "User-Agent":
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
            },  # headers
            verify=True,
            timeout=0.5)
        data = BeautifulSoup(resp.text, u"html.parser")
        # pprint(data.find_all(face="Verdana, Arial, Helvetica, sans-serif", size="5"))
        o_ip = data.get_text()
        wf.add_item(u'External IP: {}'.format(o_ip), subtitle='Enter to clipboard', arg=o_ip, valid=True)

    except:
        # print(u"WWAN Offline")
        wf.add_item(u'WWAN Offline')
    wf.send_feedback()


def submain(wf):
    wf.add_item(u'Fetching...')
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    # wf.run(submain)
    sys.exit(wf.run(main))