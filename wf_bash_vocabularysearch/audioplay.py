#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: pmz
# @Date:   2018-12-26 17:42:17
# @Last Modified by:   pmz
# @Last Modified time: 2018-12-26 20:18:02
import sys
from workflow import Workflow
from playsound import playsound

reload(sys)
sys.setdefaultencoding(u'utf8')


def main(wf):
    query = wf.args[0].strip().replace(u"\\", u"")
    howjsay_audio_url = 'https://howjsay.com/mp3/{}.mp3'.format(query.lower())
    try:
        playsound(howjsay_audio_url)
    except:
        print "Audio not found"
    # wf.send_feedback()


if __name__ == u'__main__':
    wf = Workflow()
    sys.exit(wf.run(main))