#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: forAllBright
# @Date:   2018-12-22 23:33:32
# @Last Modified by:   forAllBright
# @Last Modified time: 2018-12-23 01:02:02

import os
import plistlib


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


def updatePlist():
    fileName = os.path.expanduser('~/library/preferences/com.eusoft.eudic.plist')
    if os.path.exists(fileName):
        pl = plistlib.readPlist(fileName)
        previous_main_left_count = pl['MAIN_TimesLeft']
        present_main_left_count = 820711
        pl['MAIN_TimesLeft'] = present_main_left_count
        plistlib.writePlist(pl, fileName)
    else:
        print('%s does not exist, so can\'t be read' % fileName)

    if plistlib.readPlist(fileName)['MAIN_TimesLeft'] == present_main_left_count:
        print(bcolors.GREEN + "\n****Update main_timeleft successfully****")
        print("Main_TimeLeft: {}\n".format(present_main_left_count) + bcolors.ENDC)
    else:
        print(bcolors.RED + "\nUpdate main_timeleft fail\n" + bcolors.ENDC)


if __name__ == '__main__':
    updatePlist()
