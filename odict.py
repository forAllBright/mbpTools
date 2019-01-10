# encoding: utf-8

import sys
import requests
# import textwrap
from bs4 import BeautifulSoup
from pprint import pprint

def main():
    args = ['Wonder']
    vocab_url = "http://www.vocabulary.com/dictionary/{0}".format(args[0])
    mw_url = "http://www.merriam-webster.com/dictionary/{0}".format(args[0])
    howjsay_url = "http://www.howjsay.com/index.php?word={0}".format(args[0])

    r = requests.get(vocab_url)
    soup = BeautifulSoup(r.text, "html.parser")
    # Vocab short definition
    short_def = soup.select('div.section.blurb > p.short')
    if len(short_def) > 0:
        short_def_text = short_def[0].text
    def_grps = soup.select('div.section.definition > div.group')
    max_def_count = 3
    write2file = args[0] + '\n' + short_def_text + '\n\n'
    for def_grp in def_grps:
        def_count = 0
        for def_ in def_grp.select('div.ordinal h3.definition'):
            # print(''.join([i for i in def_.text if (i.isalpha() or i==' ' or i.isnumeric())]))
            tmp = ''.join([i for i in def_.text if (i.isalpha() or i==' ' or i.isnumeric())]) + '\n'
            write2file = write2file + tmp
    with open("temp.txt", 'w') as f:
        f.write(write2file)

main()