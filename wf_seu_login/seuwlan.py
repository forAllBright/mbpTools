# -*- coding: utf-8 -*-

from workflow import Workflow, web
import sys

ICON_DEFAULT = 'FLOW_ICON.png'
ICON_LOGIN = 'ICON_LOGIN.png'
ICON_IP = 'ICON_IP.png'
ICON_ERROR = 'ICON_ERROR.png'
ICON_PROCESS = 'ICON_PROCESS.png'

reload(sys)
sys.setdefaultencoding('utf8')


def main(wf):
    query = wf.args[0].strip().replace("\\", "")
    if not query:
        wf.add_item(title='seu-wlan login', arg='_',valid=True)
        wf.send_feedback()
        return 0

    if query in ("login", "logout", "status", "li", "lo", "st"):
        wf.add_item(
            title="Processing", arg=query, valid=True, icon=ICON_PROCESS)
        wf.send_feedback()
    else:
        wf.add_item(
            title="Invalid Parameter", arg=None, valid=True, icon=ICON_ERROR)
        wf.send_feedback()
        # return 0


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
