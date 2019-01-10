#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: forAllBright
# @Date:   2018-12-14 13:13:45
# @Last Modified by:   forAllBright
# @Last Modified time: 2018-12-14 17:13:10
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--name', required=False, help="NAME")
args = parser.parse_args()

if args.name is None:
    print("NONE")
else:
    print(args.name)
