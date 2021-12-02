# coding:utf-8
# import urllib
import MySQLdb
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
def get_content(xuebu):
    url = "https://yswk.csdl.ac.cn/qiantai/Shouye_yuanshiminglu.action?xuebu=" + str(xuebu)
    random_header = random.choice(headers)
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    req = urllib2.Request(url)
    req.add_header("User-Agent", random_header)
    req.add_header("Host", "yswk.csdl.ac.cn")
    req.add_header("Referer", "https://yswk.csdl.ac.cn/")
    req.add_header("GET", url)
    try:
        contentfirst = opener.open(req)
        if contentfirst.getcode() != 200:
            return None
        content = contentfirst.read().decode('utf-8')
        print content
        # time.sleep(2)
        # soup = BeautifulSoup(content, "lxml")
        # # 定义返回的json字符串
        # print(soup)
        # return content
        return json.dumps(content, encoding="UTF-8", ensure_ascii=False)
    except urllib2.URLError, e:
        print e.reason


if __name__ == '__main__':
    db = MySQLdb.connect("localhost", "root", "123456", "scweb_compare")
    cursor = db.cursor()
    db.set_character_set('utf8')
    # dbc.execute('SET NAMES utf8;')
    # dbc.execute('SET CHARACTER SET utf8;')
    # dbc.execute('SET character_set_connection=utf8;')

    # print '%s的年龄是%d岁'  %('', None)

    sql = "INSERT INTO scweb_compare.casyswk(username,  isFinish, number, pname, isdead,xuebu) VALUES ('%s', '%s','%s', '%s', '%s','%s')" % (
        'null', '2', 'testnumber', 'pname', str(1), '10')

    try:
        cursor.execute(sql)
        db.commit()
        print "success"
    except Exception, e:
        db.rollback()
        db.close()
        print repr(e)
