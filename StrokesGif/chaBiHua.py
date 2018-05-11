# -*-coding:utf-8-*-
# import urllib
import urllib
import urllib2
import random
import time
from bs4 import BeautifulSoup
import requests
import lxml
import re
import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import cookielib

headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"
]


# https://zh.wiktionary.org/wiki/%E5%A5%BD
def get_content(id, headers):
    url = "http://www.52tinggushi.com/html/bihua/{}.html".format(id)
    random_header = random.choice(headers)
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    req = urllib2.Request(url)
    req.add_header("User-Agent", random_header)
    req.add_header("Host", "www.52tinggushi.com")
    req.add_header("Referer", "http://www.52tinggushi.com/")
    req.add_header("GET", url)
    try:
        contentfirst = opener.open(req)
        if contentfirst.getcode() != 200:
            return None
        content = contentfirst.read().decode('utf-8')
        time.sleep(5)
        soup = BeautifulSoup(content, "lxml")
        gif = soup.select("#pinyinImg")[0]['src']
        download_gif(id,gif)
        print(gif)

    except urllib2.URLError, e:
        print e.reason


# 保存图片
def download_gif(id, gifUrl):
    web = urllib.urlopen(gifUrl)
    data = web.read()
    f = open('C:\Users\liangxiaolx\Desktop\ChineseWord\dataOut/' + str(id) + '.gif', "wb")
    f.write(data)
    f.close()


if __name__ == '__main__':
    print "hello"
    for num in range(1378, 3500, 1):
        print "id:", num
        print(num)
        get_content(num, headers)
