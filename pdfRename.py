#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: pmz
# @Date:   2018-12-21 10:26:03
# @Last Modified by:   forAllBright
# @Last Modified time: 2018-12-21 11:19:10


import sys
import importlib
importlib.reload(sys)

from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import *
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

'''
解析pdf文件，获取文件中包含的各种对象
'''


# 解析pdf文件函数
def parse(pdf_path):
    fp = open(pdf_path, 'rb')  # 以二进制读模式打开
    # 用文件对象来创建一个pdf文档分析器
    parser = PDFParser(fp)
    # 创建一个PDF文档
    doc = PDFDocument()
    # 连接分析器 与文档对象
    parser.set_document(doc)
    doc.set_parser(parser)

    # 提供初始化密码
    # 如果没有密码 就创建一个空的字符串
    doc.initialize()

    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDf 资源管理器 来管理共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # 用来计数页面，图片，曲线，figure，水平文本框等对象的数量
        num_page, num_image, num_curve, num_figure, num_TextBoxHorizontal = 0, 0, 0, 0, 0


        layouts=[]
        # 循环遍历列表，每次处理一个page的内容
        for page in doc.get_pages():  # doc.get_pages() 获取page列表
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            layouts.append(layout)
        results = ""
        # y = list(layouts[0])[0]
        z = list(layouts[0])[1]
        for i in (z,):
            if isinstance(i, LTTextBoxHorizontal):  # 获取文本内容
                results = results + i.get_text()
        print(results)




if __name__ == '__main__':
    pdf_path = r'/Users/pmz/Desktop/19_IIS190208.pdf'
    parse(pdf_path)
