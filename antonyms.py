#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Andrew Starodubtsev'
__email__ = 'devtech@illucent.info'
__revision__ = '$Revision: 0.000000001 $'
__doc__ = 'antonyms search'
__usage__ = 'this module should be run via the command line'


"""
plans to replace endpoint to wiktionary.org
https://ru.wiktionary.org/wiki/%D0%B0%D0%BD%D1%82%D0%BE%D0%BD%D0%B8%D0%BC
"""


import sys
import argparse
import urllib.parse
import urllib2
import base64
import cookielib
import string
import codecs
import locale

from unicodedata import *
from bs4 import BeautifulSoup

# os.system("clear")

reload(sys)
sys.setdefaultencoding('utf8')


def build_argparser():
		parser = argparse.ArgumentParser()
		parser.add_argument('-w', dest='word', help="word search antonym for" )
		parser.add_argument('-l', dest='lang', help="lanuage search antonym for", default='ru' )
		return parser

	
def print_to_console(text):
    enc = locale.getdefaultlocale()[1] or "utf-8"
    try:
        print(text.encode(enc, errors="backslashreplace"))
    except (LookupError, UnicodeEncodeError):
        # Unknown encoding or encoding problem. Fallback to ascii
        print(text.encode("ascii", errors="backslashreplace"))

	
def getAntonymRu(word, *lang):

	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'

	headers = {
	'User-Agent' : user_agent,
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Charset': 'windows-1251,utf-8;q=0.7,*;q=0.3',
	'Accept-Encoding':'none',  # 'gzip, deflate',
	'Accept-Language': 'ru-RU,ru;q=0.8',
	'Content-Type': 'application/x-www-form-urlencoded',
	'Connection': 'keep-alive'
	}

	# Input parameters we are going to send
	params = {}
	params['lv'] = str('x').encode('utf-8')
	params['word'] = word.lower().encode('utf-8')

	# Use urllib to encode the payload
	encoded = urllib.parse.urlencode(params)

	url = 'http://www.gramota.ru/slovari/dic/?'
	req = urllib2.Request(url+encoded, data=encoded, headers=headers)

	# Make the request and read the response
	resp = urllib2.urlopen(req).read()
	soup = BeautifulSoup(resp, 'html.parser')
	# 'inside block-content'
	text=[]
	for div in soup.find_all('div', attrs={'style': 'padding-left:50px'}):
		d = div.get_text(strip=False).decode('utf-8')
		# text.append(d[:])
		print_to_console(d[:])

def main():
    args = build_argparser().parse_args()
    getAntonymRu(args.word, args.lang)
    sys.exit(-1)


if __name__ == '__main__':
    main()
