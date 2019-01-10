# -*- coding: utf-8 -*-

from __future__ import absolute_import
import sys
import requests
# import textwrap
from workflow import Workflow
from bs4 import BeautifulSoup
import logging

reload(sys)
sys.setdefaultencoding(u'utf8')


def main(wf, short_def_text=''):
    logger = logging.getLogger('http connection')
    query = wf.args[0].strip().replace(u"\\", u"")
    vocab_url = u"https://www.vocabulary.com/dictionary/{0}".format(query)
    mw_url = u"https://www.merriam-webster.com/dictionary/{0}".format(query)
    howjsay_url = u"https://www.howjsay.com/index.php?word={0}".format(query)

    try:
        proxies = {'https': "socks5://127.0.0.1:1086"}
        r = requests.get(
            vocab_url,
            headers={
                "User-Agent":
                r"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
            },
            timeout=2,
            proxies=proxies)
        soup = BeautifulSoup(r.text, u"html.parser")
    except Exception as e:
        logger.error("Failed to connect server: " + str(e))
        wf.add_item(title="Connection ERROR")
        wf.send_feedback()
        return 0
    # Vocab short definition
    short_def = ''
    short_def = soup.select(u'div.section.blurb > p.short')
    write2file_list = []
    write2file_list.append(query)
    if len(short_def) > 0:
        short_def_text = short_def[0].text
        write2file_list.append(short_def_text)
        write2file_list.append(' ')
        wf.add_item(
            title="[CMD+L] | {0} ...".format(short_def_text[:30]),
            largetext=short_def_text,
            arg=query,
            valid=True)
        def_grps = soup.select(u'div.section.definition > div.group')
        for def_grp in def_grps:
            for def_ in def_grp.select(u'div.ordinal h3.definition'):
                definition = def_.get_text('  |→  ', strip=True)
                wf.add_item(title=definition, valid=False)
                write2file_list.append(definition)
    else:
        wf.add_item(title="Not found...")
    wf.send_feedback()
    write2file = '\n'.join(write2file_list)
    with open('temp.txt', 'w') as f:
        f.write(write2file)



if __name__ == u'__main__':
    wf = Workflow()
    sys.exit(wf.run(main))