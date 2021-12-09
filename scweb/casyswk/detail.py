# -*-coding:utf-8-*-
# import urllib
import json
import random
import ssl
import sys
import time
import urllib
import urllib2

import MySQLdb
from bs4 import BeautifulSoup

from utils.JsonUtil import listToJson

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
def get_content(id, number):
    url = "https://yswk.csdl.ac.cn/qiantai/Shouye_zhanshi.action?id=" + str(number)
    random_header = random.choice(headers)
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    req = urllib2.Request(url)
    req.add_header("User-Agent", random_header)
    req.add_header("Host", "yswk.csdl.ac.cn")
    req.add_header("Referer", "https://yswk.csdl.ac.cn/")
    req.add_header("GET", url)
    while True:
        try:
            print "start..."
            contentfirst = opener.open(req, timeout=15)
            print contentfirst.getcode()
            if contentfirst.getcode() != 200:
                return None
            print contentfirst
            print "start contentfirst.read()..."
            content = contentfirst.read().decode('utf-8')
            # time.sleep(2)
            print "start soup..."
            soup = BeautifulSoup(content, "lxml")
            # 定义返回的json字符串
            scDetail = {}
            gaishuList = soup.findAll(name="p", attrs={"class": "gaishu"})
            scDetail['gaishu'] = gaishuList[0].get_text()
            gaishu_img = []
            gaishu_href = []
            for item in gaishuList:
                if item.find(name="img") != None:
                    gaishu_img.append(item.find(name="img")['src'])
                    gaishu_href.append(item.find(name="a")['href'])
            scDetail['gaishu-img'] = ','.join(gaishu_img) if len(gaishu_img) > 0 else '';
            scDetail['gaishu-href'] = ','.join(gaishu_href) if len(gaishu_href) > 0 else '';
            scDetail['person-type'] = soup.find(name="p", attrs={"class": "person-type"}).get_text()
            person_slider_top = [];
            for item in soup.find(name="div", attrs={"class": "person-slider-top"}).findAll(name="li"):
                person_slider_top.append(item.get_text());
            scDetail['person-slider-top'] = ','.join(person_slider_top).replace("\n", "")
            # 各项资料数量
            detailList = soup.findAll(name="div", attrs={"class": "per-cols clearfix"})
            classnameList = []
            for item in detailList:
                typenameList = [];
                classnameDetail = {}
                aList = item.findAll(name="a")
                for a in aList:
                    if a.find(name="em", attrs={"id": "cczz"}) != None:
                        typenameDetail = {};
                        typenameDetail['key'] = a.find(name="span").get_text()
                        typenameDetail['value'] = a.find(name="em").get_text().strip('(').strip(')')
                        typenameList.append(typenameDetail)
                if item.find(name="h4") != None:
                    classnameDetail['key'] = item.find(name="h4").next.replace("\t", "").replace("\n", "")
                    classnameDetail['list'] = typenameList;
                    classnameList.append(classnameDetail)
            scDetail['classnameListJson'] = listToJson(classnameList)
            scDetail['classnameList'] = classnameList
            contentfirst.close()
            return scDetail
        except urllib2.URLError, e:
            print 'URLError...'
            print e.reason
        except ssl.SSLError, e:
            print 'SSLError...'
            print e



def spider(id):
    db = MySQLdb.connect("localhost", "root", "123456", "scweb_compare")
    cursor = db.cursor()
    db.set_character_set('utf8')
    sql = "select number from scname_casyswk where id>" + str(id) + " order by id"
    # result = get_content('2019A03')
    # print result
    try:
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for it in results:
            # time.sleep(random.randint(12, 50))
            print it[0]
            number = it[0]
            result = get_content(id, number)
            print result.get('gaishu')
            sql = "INSERT INTO scweb_compare.scdetail_casyswk( gaishu, record_time,number ,gaishu_img, gaishu_href, person_type, person_slider_top,classname_list)  VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                db.escape_string(result.get('gaishu')), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                number,
                db.escape_string(result.get('gaishu-img')), db.escape_string(result.get('gaishu-href')),
                db.escape_string(result.get('person-type')), db.escape_string(result.get('person-slider-top')),
                db.escape_string(result.get('classnameListJson')))
            try:
                cursor.execute(sql)
                db.commit()
                print "success"
            except Exception, e:
                db.rollback()
                db.close()
                print repr(e)

            classnameList = result.get("classnameList");
            for item in classnameList:
                classname = item.get('key')
                for type in item.get('list'):
                    typename = type.get('key')
                    value = type.get('value')
                    sql = "INSERT INTO scweb_compare.scdetail_count_casyswk(  classname, typename, value, number, record_time)  VALUES ('%s', '%s', '%s', '%s', '%s')" % (
                        db.escape_string(classname), db.escape_string(typename), db.escape_string(value), number,
                        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                    try:
                        cursor.execute(sql)
                        db.commit()
                        print "success"
                    except Exception, e:
                        db.rollback()
                        db.close()
                        print repr(e)
        print "all success"
    except Exception, e:
        db.rollback()
        db.close()
        print repr(e)


if __name__ == '__main__':
    print "hello"
    spider(976)
