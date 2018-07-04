# -*-coding:utf-8-*-
# import urllib
import random
import sys
import time
import urllib
import urllib2

from bs4 import BeautifulSoup

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


# https://mzidian.911cha.com/?q=好
def get_content(id, headers):
    url = id
    random_header = random.choice(headers)
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    req = urllib2.Request(url)
    req.add_header("User-Agent", random_header)
    req.add_header("Host", "mzidian.911cha.com")
    req.add_header("Referer", "https://mzidian.911cha.com/")
    req.add_header("GET", url)
    try:
        contentfirst = opener.open(req)
        if contentfirst.getcode() != 200:
            return None
        content = contentfirst.read().decode('utf-8')
        time.sleep(1)
        soup = BeautifulSoup(content, "lxml")
        pinyinList = soup.find_all('li')
        for pinyin in pinyinList:
            pinyin = pinyin.get_text()
            if pinyin == "":
                continue
            if pinyin == "拼音查字":
                break
            f = open('C:\Users\liangxiaolx\Desktop\ChineseWord\mzidian\dataOut/pinyin.txt', 'a')
            f.write(pinyin + '\n')
            f.close()
            print(pinyin)
    except urllib2.URLError, e:
        print e.reason


if __name__ == '__main__':
    url = "https://mzidian.911cha.com/pinyin.html"
    get_content(url, headers)
