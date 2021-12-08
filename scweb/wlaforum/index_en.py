# -*-coding:utf-8-*-
# import urllib
import json
import random
import sys
import time
import urllib
import urllib2

import MySQLdb
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
def get_content():
    url = "https://en.wlaforum.com/scientists.html"
    random_header = random.choice(headers)
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    req = urllib2.Request(url)
    req.add_header("User-Agent", random_header)
    req.add_header("Host", "en.wlaforum.com")
    req.add_header("Referer", "https://en.wlaforum.com/")
    req.add_header("GET", url)
    try:
        contentfirst = opener.open(req)
        if contentfirst.getcode() != 200:
            return None
        content = contentfirst.read().decode('utf-8')
        # time.sleep(2)
        soup = BeautifulSoup(content, "lxml")
        # 定义返回的json字符串
        laureateslist = soup.findAll(name="a", attrs={"class": "laureates-item"})
        sclist = []
        for item in laureateslist:
            sc = {};
            scname = item.find(name="div", attrs={"class": "laureates-name"}).get_text()
            award = item.find(name="div", attrs={"class": "laureates-award"}).get_text()
            sc['scname'] = scname
            sc['award'] = award
            sclist.append(sc)
        return sclist
    except urllib2.URLError, e:
        print e.reason


if __name__ == '__main__':
    print "hello"
    db = MySQLdb.connect("localhost", "root", "123456", "scweb_compare")
    cursor = db.cursor()
    db.set_character_set('utf8')
    result = get_content()
    for item in result:
        print item.get('scname')
        sql = "INSERT INTO scweb_compare.scname_wlaforum_en( scname, award)  VALUES ('%s', '%s')" % (
            db.escape_string(item.get('scname')), db.escape_string(item.get('award')))
        try:
            cursor.execute(sql)
            db.commit()
            print "success"
        except Exception, e:
            db.rollback()
            db.close()
            print repr(e)

