#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: pmz
# @Date:   2018-12-07 15:49:26
# @Last Modified by:   forAllBright
# @Last Modified time: 2018-12-16 20:45:20
"""[summary]
__        __   _
\ \      / /__| | ___ ___  _ __ ___   ___
 \ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \
  \ V  V /  __/ | (_| (_) | | | | | |  __/
   \_/\_/ \___|_|\___\___/|_| |_| |_|\___|

This script is for axel downloading file from baidu-cloud with specific
download link be copied in clipboard.

'''
Before using this script on terminal, the specific download link should be stored
in clipboard. An example of this kind link is as below:
aria2c -c -s10 -k1M -x16 --enable-rpc=false -o "Screens_4_4.6.5_xclient.info.dmg" --header "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36" --header "Referer: https://pan.baidu.com/disk/home" --header "Cookie: BDUSS=p3cFNUeGRmN1c4ZHdHSk5tMWZsVGlGQ21XSH5CMWlNRDktcnMyRkNCRjB5eTFjQVFBQUFBJCQAAAAAAAAAAAEAAAAqkTkR1uzG1cP3sKEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHQ-Blx0PgZcUX; pcsett=1544270308-e4a723ec35097e43e758d9613e0d8051" "https://d.pcs.baidu.com/file/0172f3e832b1cd2d9f1776308089d4c0?fid=4185473307-250528-979353614800332&dstime=1544183912&rt=sh&sign=FDtAERV-DCb740ccc5511e5e8fedcff06b081203-1kjmbxuDLQT%2FEd6vh5TedlDXRGY%3D&expires=8h&chkv=1&chkbd=0&chkpc=&dp-logid=7904863798832747453&dp-callid=0&shareid=478603389&r=440964212"
Then just run this script on terminal and axel command output will be flushed on screen.
Glad to get what you want.
'''
"""

import clipboard
import re
import os
import argparse

parser = argparse.ArgumentParser(
    description="This is the usage help of this script.")
parser.add_argument(
    "-n",
    "--axel_thread_num",
    required=False,
    type=int,
    help="The number of axel threads, default is 10")
parser.add_argument("-d","--debug",action="store_true", help="Debug mode on")
args = parser.parse_args()


class InvalidDownloadLinkParse(Exception):
    pass


class InvalidAccessClipBoard(Exception):
    pass


class Axel_parser:
    """[summary]

    [Axel download Class for parsing clipboard download link and download woth axel]
    """

    def __init__(self, save_path_prefix, thread_num=10):
        self.thread_num = thread_num
        self.text = ""
        self.terminal_cmd = ""
        self.save_path_prefix = save_path_prefix
        self.fullpath = ""
        self.download_file_name = ""

    def parse(self):
        """[summary]

        [Parse clipboard download link and do axel process]

        Raises:
            InvalidAccessClipBoard -- [Clipboard asscess exception]
            InvalidDownloadLinkParse -- [Exception of clipboard download link does not conform requirement]
        """
        try:
            self.text = clipboard.paste()
        except:
            raise InvalidAccessClipBoard("clipboard access fail")
        assert self.text != "", "No valid cliped text"
        pattern = r'-o (.*) --header ("User-Agent:.*) --header ("Cookie:.*?") (.*)'
        search_obj = re.search(pattern, self.text)
        try:
            self.download_file_name = search_obj.group(1)[1:-1]
            self.fullpath = r'"{0}/{1}"'.format(self.save_path_prefix,
                                                search_obj.group(1)[1:-1])
            if search_obj.group(1) and search_obj.group(
                    2) and search_obj.group(3) and search_obj.group(4):
                self.terminal_cmd = r'axel -a -o {0} --header {1} --header {2} {3} -n {4}'.format(
                    self.fullpath, search_obj.group(2), search_obj.group(3),
                    search_obj.group(4), self.thread_num)
            else:
                print("clipboard text parse fail")
                os._exit(1)
        except:
            raise InvalidDownloadLinkParse(bcolors.FAIL + "clipboard download link parsing error")
            os._exit(1)

    def axel_monitor(self):
        """[summary]

        [Flush print the axel native log to terminal screen]
        """
        self.parse()
        if args.debug:
            print(self.terminal_cmd)
        else:
            pass
        print(bcolors.OKGREEN + '''
                 ____  _             _   _
                / ___|| |_ __ _ _ __| |_(_)_ __   __ _
                \___ \| __/ _` | '__| __| | '_ \ / _` |
                 ___) | || (_| | |  | |_| | | | | (_| |
                |____/ \__\__,_|_|   \__|_|_| |_|\__, |
                                                 |___/
              ''' + bcolors.ENDC)

        os.system(self.terminal_cmd)

    def overwrite_download(self, filefolder, filepath):
        """[summary]

        [Check if the file to be downloaded this time has been in the folder
        and prompt for user's input to overwrite this file or cancel this downloading]

        Returns:
            bool -- [Indicator for overwrite an downloaded file or not]
        """
        folderfiles = os.listdir(filefolder)
        if self.download_file_name in folderfiles:
            user_input = input("The same named file has been in your folder,are you sure you want to overwrite it??? Type " + bcolors.RED + "'yes'" + bcolors.ENDC + " to continu and " + bcolors.BLUE + "'no'" + bcolors.ENDC + " to cancel this download ->>> ")
            assert user_input in ["yes", "no"], bcolors.FAIL + "Input must be 'yes' or 'no'" + bcolors.ENDC
            if user_input == "yes":
                os.remove(r'{}'.format(filepath))
                return True
            else:
                return False
        else:
            return True

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RED = '\033[1;31;43m'
    BLUE = '\033[1;37;44m'

if __name__ == "__main__":
    download_folder = r'{0}/Downloads'.format(os.environ['HOME'])
    if args.axel_thread_num:
        axel_p = Axel_parser(
            save_path_prefix=download_folder, thread_num=args.axel_thread_num)
    else:
        axel_p = Axel_parser(save_path_prefix=download_folder)
    overwrite_check_flag = axel_p.overwrite_download(axel_p.save_path_prefix, axel_p.fullpath)
    if overwrite_check_flag:
        axel_p.axel_monitor()
        print(bcolors.OKGREEN + '''
                  ____                      _      _           _
                 / ___|___  _ __ ___  _ __ | | ___| |_ ___  __| |
                | |   / _ \| '_ ` _ \| '_ \| |/ _ \ __/ _ \/ _` |
                | |__| (_) | | | | | | |_) | |  __/ ||  __/ (_| |
                 \____\___/|_| |_| |_| .__/|_|\___|\__\___|\__,_|
                         |_|
              ''' + bcolors.ENDC)
    else:
        print(bcolors.WARNING + '''
                 ____                      _                 _   ____  _
                |  _ \  _____      ___ __ | | ___   __ _  __| | / ___|| |_ ___  _ __
                | | | |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` | \___ \| __/ _ \| '_ \
                | |_| | (_) \ V  V /| | | | | (_) | (_| | (_| |  ___) | || (_) | |_) |
                |____/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_| |____/ \__\___/| .__/
                                                                               |_|
            ''' + bcolors.ENDC)
