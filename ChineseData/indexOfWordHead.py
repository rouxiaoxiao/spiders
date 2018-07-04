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
        wordHead_file = open("C:\Users\liangxiaolx\Desktop\ChineseWord\mzidian\dataOut\wordHead.txt", "a")
        contentfirst = opener.open(req)
        if contentfirst.getcode() != 200:
            return None
        content = contentfirst.read().decode('utf-8')
        time.sleep(1)
        soup = BeautifulSoup(content, "lxml")
        wordHeadList = soup.find_all('a')
        print(wordHeadList)
        wordHead = ""
        url_suffix = ""
        for line in wordHeadList:
            print("line:" + str(line))
            print(url)
            if (line is None) or (line == ""):
                continue
            if str(line).find("点击查看全部拼音") >= 0:
                break
            # 拼音列表中存在为汉字和图片两种
            if line.find('img'):
                wordHead = line.find('img').get('alt')
            elif line.get_text() != "":
                wordHead = line.get_text()
                if line.find('span'):
                    spanList = line.find_all('span')
                    print(spanList)
                    for span in spanList:
                        wordHead = wordHead.replace(span.get_text(), "")
            url_suffix = line.get('href')
            print("url_suffix:" + url_suffix)
            print("wordHead:" + wordHead)
            wordHead_file.write(wordHead + "####" + url_suffix + "\n")
        wordHead_file.close()

    except urllib2.URLError, e:
        print e.reason


if __name__ == '__main__':
    pinyin_file = open("C:\Users\liangxiaolx\Desktop\ChineseWord\mzidian\dataIn\pinyin.txt")
    for pinyin in pinyin_file:
        pinyin = pinyin.replace("\n", "")
        url = "https://mzidian.911cha.com/pinyin_{}.html".format(pinyin)
        get_content(url, headers)
    pinyin_file.close()
