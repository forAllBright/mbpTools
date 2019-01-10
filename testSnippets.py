#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: forAllBright
# @Date:   2018-12-14 13:13:45
# @Last Modified by:   forAllBright
# @Last Modified time: 2018-12-24 23:31:24
# import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument('-n', '--name', required=False, action="store_true", help="NAME")
# args = parser.parse_args()

# if args.name is None:
#     print("NONE")
# else:
#     print(args.name)

# from PIL import Image
# filename = "/Users/pmz/gitee/Blogpics/test2.png"
# with Image.open(filename) as img:
#     print(img.size)
#     new = img.resize((500,500))
#     print(new.size)
#     new.save("/Users/pmz/gitee/Blogpics/new.png", 'PNG')

import git
import time
import subprocess
import os
import threading

# g = git.cmd.Git(r"/Users/pmz/gitee/Blogpics")
# g.execute(["git", "add", "testtttttt.png"])
# g.execute(["git", "commit", "-m", "testtttttt.png"])
# g.execute(["git", "push", "origin", "master"])

# repo = git.Repo(r"/Users/pmz/gitee/Blogpics")
# print(repo.remotes.origin.url)
# repo.remotes.origin.fetch()
# origin = repo.remote('origin')
# print(origin.url)


def checkGitConnection():
    repo = git.Repo(r"{}".format("/Users/pmz/gitee/Blogpics"))
    try:
        repo.remotes.origin.fetch()
    except:
        pass
        return False
    return True


# def wait_timeout(seconds):
#     """Wait for a process to finish, or raise exception after timeout"""
#     start = time.time()
#     end = start + seconds
#     interval = min(seconds / 1000.0, .25)
#     with subprocess.Popen(['yes']) as procl:
#         while True:
#             result = procl.poll()
#             if result is not None:
#                 return result
#             if time.time() >= end:
#                 os._exit(1)
#             time.sleep(interval)

# wait_timeout(10)
# # print(checkGitConnection())

# def hello():
#     while True:
#         pass
#     print("hello, world")

# t = threading.Timer(3.0, hello)
# t.start()



# while True:
#     color = input("Color code: \n")
#     print('\033[{}m'.format(color) + "HELLO" + '\033[0m')



#
# class bcolors:
#     # Colors
#     PURPLE = '\033[1;35;1m'
#     RED = '\033[1;31;1m'
#     BLUE = '\033[1;34;1m'
#     GREEN = '\033[1;32;1m'
#     CYAN = "\033[1;36;1m"
#     YELLOW = "\033[1;33;1m"
#     BLACK = "\033[1;30;1m"
#     WHITE = "\033[1;37;1m"
#     # Font effects
#     ENDC = '\033[0m'
#     BOLD = '\033[1m'
#     UNDERLINE = '\033[4m'
#     NEFATIVE1 = '\033[3m'
#     NEFATIVE2 = '\033[5m'
#     # Background colors
#     BACKGROUND_BLACK = "\033[;;40m"
#     BACKGROUND_RED = "\033[;;41m"
#     BACKGROUND_GREEN = "\033[;;42m"
#     BACKGROUND_YELLOW = "\033[;;43m"
#     BACKGROUND_BLUE = "\033[;;44m"
#     BACKGROUND_PURPLE = "\033[;;45m"
#     BACKGROUND_CYAN = "\033[;;46m"
#     BACKGROUND_WHITE = "\033[;;47m"
#
# foo = [x for x in dir(bcolors()) if not x.startswith('__')]
# print(foo)
#
# for color in foo:
#     print(color)
#     print("\n{}Hello,World!{}\n".format(
#         getattr(bcolors(), color), bcolors.ENDC))
#
#



# 2018-12-24-23:18:38
import requests
from bs4 import BeautifulSoup
from pprint import pprint

resp = requests.get(
    "https://www.vocabulary.com/dictionary/wonder",
    headers={
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    },  # headers
    verify=True,
    timeout=1)
data = BeautifulSoup(resp.text, "html.parser")
pprint(data.head)
pprint("-------------------------------------------------------------")
pprint(data.select("head > link"))