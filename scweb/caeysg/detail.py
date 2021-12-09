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


# 个人主页
def get_content(id, number):
    url = "https://ysg.ckcest.cn/html/details/" + str(number) + "/index.html"
    random_header = random.choice(headers)
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    req = urllib2.Request(url)
    req.add_header("User-Agent", random_header)
    req.add_header("Host", "ysg.ckcest.cn")
    req.add_header("Referer", "https://ysg.ckcest.cn/")
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
            detail_frame = []
            detail_frame_li_list = soup.find(name="div", attrs={"class": "detail_frame"}).findAll(name="li")
            for item in detail_frame_li_list:
                detail_frame_item = {}
                classname = item.get_text().replace("\n", "")
                detail_frame_item['key'] = classname
                subNavs = item.find(name="div", attrs={"class": "subNavs"})
                if subNavs != None:
                    subNavs_div = subNavs.findAll(name="div")
                    subItemList = []
                    for subItem in subNavs_div:
                        subItemObj = {}
                        sub_data_url = subItem['data-url']
                        sub_data_name = subItem['data-name']
                        subItemObj['key'] = sub_data_name
                        subItemObj['value'] = sub_data_url
                        subItemList.append(subItemObj)
                    detail_frame_item['list'] = subItemList
                    detail_frame.append(detail_frame_item)
            scDetail['detail_frame'] = detail_frame
            scDetail['detail_frame_json'] = listToJson(detail_frame)
            # 个人信息
            particular_info = soup.find(name="div", attrs={"class": "particular_info"})
            top_part = particular_info.find(name="div", attrs={"class": "top_part"})
            acInfo = top_part.find(name="div", attrs={"class": "acInfo"})
            acInfo_div = acInfo.findAll(name="div")
            scname = acInfo_div[0].findAll(name="h4")[1].get_text().replace("\n", "").replace("\r", "")
            nationality = acInfo_div[1].findAll(name="h4")[1].get_text().replace("\n", "").replace("\r", "")
            sex = acInfo_div[2].findAll(name="h4")[1].get_text().replace("\n", "").replace("\r", "")
            birthplace = ','.join(acInfo_div[3].findAll(name="h4")[1].get_text().replace("\n", "").replace("\r", "").strip().split())
            birthday = acInfo_div[4].findAll(name="h4")[1].get_text().replace("\n", "").replace("\r", "").strip()
            scDetail['scname'] = scname
            scDetail['nationality'] = nationality
            scDetail['sex'] = sex
            scDetail['birthplace'] = birthplace
            scDetail['birthday'] = birthday
            bottome_part = particular_info.find(name="div", attrs={"class": "bottome_part"})
            bottome_part_div = bottome_part.findAll(name="div")
            electedyear = ','.join(bottome_part_div[0].findAll(name="h4")[1].get_text().replace("\n", "").replace("\r", "").strip().split())
            faculty =','.join(bottome_part_div[1].findAll(name="h4")[1].get_text().replace("\n", "").replace("\r", "").strip().split())
            links_a = bottome_part_div[1].findAll(name="h4")[1].findAll(name="a")
            linkList = []
            links = ''
            for item in links_a:
                linkList.append(item['href'])
            if (len(linkList) > 0):
                links = ','.join(linkList)
            scDetail['electedyear'] = electedyear
            scDetail['faculty'] = faculty
            scDetail['links'] = links
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
    sql = "select acInfoId from scname_caeysg where id>" + str(id) + " order by id"
    # result = get_content('2019A03')
    # print result
    try:
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for it in results:
            # time.sleep(random.randint(12, 50))
            print it[0]
            acInfoId = it[0]
            result = get_content(id, acInfoId)
            print result.get('gaishu')
            sql = "INSERT INTO scweb_compare.scdetail_caeysg( record_time,acInfoId ,detail_frame, scname, nationality, sex, birthplace, birthday, electedyear, faculty, links)  VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                acInfoId,
                db.escape_string(result.get('detail_frame_json')), db.escape_string(result.get('scname')),
                db.escape_string(result.get('nationality')), db.escape_string(result.get('sex')),
                db.escape_string(result.get('birthplace')), db.escape_string(result.get('birthday')),
                db.escape_string(result.get('electedyear')), db.escape_string(result.get('faculty')),
                db.escape_string(result.get('links')))
            try:
                cursor.execute(sql)
                db.commit()
                print "success"
            except Exception, e:
                db.rollback()
                db.close()
                print repr(e)

            classnameList = result.get("detail_frame");
            for item in classnameList:
                classname = item.get('key')
                for type in item.get('list'):
                    typename = type.get('key')
                    value = type.get('value')
                    sql = "INSERT INTO scweb_compare.scdetail_suburl_caeysg(  classname, typename, value, acInfoId, record_time)  VALUES ('%s', '%s', '%s', '%s', '%s')" % (
                        db.escape_string(classname), db.escape_string(typename), db.escape_string(value), acInfoId,
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
    spider(0)
