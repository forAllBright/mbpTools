# -*- coding: utf-8 -*-

from __future__ import absolute_import
import sys
import requests
# import textwrap
from workflow import Workflow
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding(u'utf8')


def main(wf, short_def_text=''):
    query = wf.args[0].strip().replace(u"\\", u"")

    vocab_url = u"http://www.vocabulary.com/dictionary/{0}".format(query)
    mw_url = u"http://www.merriam-webster.com/dictionary/{0}".format(query)
    howjsay_url = u"http://www.howjsay.com/index.php?word={0}".format(query)

    try:
        r = requests.get(vocab_url, timeout=1)
        soup = BeautifulSoup(r.text, u"html.parser")
        # Vocab short definition
        short_def = ''
        short_def = soup.select(u'div.section.blurb > p.short')
        if len(short_def) > 0:
            short_def_text = short_def[0].text
            wf.add_item(title="[CMD+L] | {0} ...".format(short_def_text[:30]), largetext=short_def_text, valid=True)
            def_grps = soup.select(u'div.section.definition > div.group')
            for def_grp in def_grps:
                for def_ in def_grp.select(u'div.ordinal h3.definition'):
                    wf.add_item(title=def_.get_text(' | ', strip=True), valid=False)
        else:
            wf.add_item(title="Searching...")
    except:
            wf.add_item(title="Searching...")
    wf.send_feedback()



if __name__ == u'__main__':
    wf = Workflow()
    sys.exit(wf.run(main))