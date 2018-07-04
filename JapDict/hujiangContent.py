# -*-coding:utf-8-*-
# import urllib
import json
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


# https://zh.wiktionary.org/wiki/%E5%A5%BD
def get_content(wordHead):
    url = "https://dict.hjenglish.com/jp/jc/" + wordHead
    random_header = random.choice(headers)
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    req = urllib2.Request(url)
    req.add_header("User-Agent", random_header)
    req.add_header("Host", "dict.hjenglish.com")
    req.add_header("Referer", "https://dict.hjenglish.com/")
    req.add_header("GET", url)
    try:
        contentfirst = opener.open(req)
        if contentfirst.getcode() != 200:
            return None
        content = contentfirst.read().decode('utf-8')
        # time.sleep(2)
        soup = BeautifulSoup(content, "lxml")
        # 定义返回的json字符串
        print(soup)
        JapWords = {}
        return json.dumps(JapWords, encoding="UTF-8", ensure_ascii=False)
    except urllib2.URLError, e:
        print e.reason


if __name__ == '__main__':
    print "hello"
    # JapWord_file = open("C:\Users\liangxiaolx\Desktop\JapWordSpider\dataOut\JapWordDesHujiang.json", "a")
    # url_data_file = open("C:\Users\liangxiaolx\Desktop\JapWordSpider\dataIn\wordHead.txt")
    i = 0
    # for line in url_data_file:
    #     i = i + 1
    #     print('~~~~~我是第' + str(i) + '个单词~~~~~位于' + line.split("####")[0] + '~~~~~' + time.asctime(
    #         time.localtime(time.time())))
    #     wordHead = line.split("####")[1].replace("\n", "")
    #     # url = line.split("####")[2].replace("\n", "")
    #     print(wordHead)
    #     howlong = [0.1, 0.2, 0.3, 0.4]
    #     time.sleep(random.choice(howlong))
    #     # get_content(url)
    #     if get_content(wordHead) != None:
    #         try:
    #             JapWord_file.write(get_content(wordHead) + "\n")
    #         except Exception, a:
    #             print a
    #             continue
    # url_data_file.close()
    # JapWord_file.close()

    # 单url测试
    JapWord_file = open("C:\Users\liangxiaolx\Desktop\JapWordSpider\dataOut\\test.json", "a")
    wordHead = '%E6%84%8F%E8%A1%A8'
    if get_content(wordHead) != None:
        try:
            JapWord_file.write(get_content(wordHead) + "\n")
        except TypeError, a:
            print a
    JapWord_file.close()

#     https://kotobank.jp/word/%E3%83%9E%E3%82%B1%E3%83%89%E3%83%8B%E3%82%A2%E5%85%B1%E5%92%8C%E5%9B%BD-1419018#E6.97.A5.E6.9C.AC.E5.A4.A7.E7.99.BE.E7.A7.91.E5.85.A8.E6.9B.B8.28.E3.83.8B.E3.83.83.E3.83.9D.E3.83.8B.E3.82.AB.29
