#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: pmz
# @Date:   2018-12-26 17:57:40
# @Last Modified by:   pmz
# @Last Modified time: 2018-12-27 10:32:21

from __future__ import absolute_import
import sys
import requests
# import textwrap
from workflow import Workflow
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding(u'utf8')


query = 'wonder'

vocab_url = u"http://www.vocabulary.com/dictionary/{0}".format(query)
mw_url = u"http://www.merriam-webster.com/dictionary/{0}".format(query)
howjsay_url = u"http://www.howjsay.com/index.php?word={0}".format(query)

r = requests.get(vocab_url, timeout=2)
soup = BeautifulSoup(r.text, u"html.parser")
print soup