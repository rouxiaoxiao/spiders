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
def get_content(url, headers):
    index = 0
    random_header = random.choice(headers)
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    req = urllib2.Request(url)
    req.add_header("User-Agent", random_header)
    req.add_header("Host", "zh.wiktionary.org")
    req.add_header("Referer", "http://zh.wiktionary.org/")
    req.add_header("GET", url)
    try:
        contentfirst = opener.open(req)
        if contentfirst.getcode() != 200:
            return None
        content = contentfirst.read().decode('utf-8')
        soup = BeautifulSoup(content, "lxml")
        # #mw-content-text > div > dl:nth-child(13) > dd > a:nth-child(2)
        # imgs = soup.findAll('a', class_="image")
        imgs = soup.select('a.image')
        imgsUrl = {}
        staticUrl = imgs[0].select('img')[0]['src']
        dynamicUrl = imgs[1].select('img')[0]['src']

        imgsUrl['static'] = staticUrl
        imgsUrl['dynamic'] = dynamicUrl
        print(imgsUrl)
        index = index + 1
        print("已解析" + index + "个网址")

    except urllib2.URLError, e:
        print e.reason


if __name__ == '__main__':
    print "hello"
    # for num in range(43481, 50000, 1):
    #     urll = "http://www.itjuzi.com/company/{}".format(num)
    #     get_content(urll,headers)
    # print(get_content("www.itjuzi.com", headers))
    with open('D:/PycharmProjects/StrokesGif/ChineseWord.txt', 'r') as f:
        data = f.readlines()  # txt中所有字符串读入data
        index = 0;
        for line in data:
            print(index)
            index = index + 1
            odom = line  # 将单个数据分隔开存好
            code = urllib.quote(odom)
            url = "https://zh.wiktionary.org/wiki/" + code
            print(url)
            get_content(url, headers)

    # string = urllib.quote('好')

    # 解码
    # result = urllib.unquote('http%3a%2f%2fwww.baidu.com%2fs%3fwd%3d%E4%BD%A0%E5%A5%BD')
