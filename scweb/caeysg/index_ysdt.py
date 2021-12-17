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

from utils.JsonUtil import listToJsonStr
from utils.StrUtil import noneToNull, noneToEmptyStr
from utils.TimeUtil import timestampToDate

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
def get_content(pageNum):
    url = "https://ysg.ckcest.cn/ysgNews/api/newsList?pageSize=12&pageNum=" + str(
        pageNum) + "&_=1639557572972"
    random_header = random.choice(headers)
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    req = urllib2.Request(url)
    req.add_header("User-Agent", random_header)
    req.add_header("Host", "ysg.ckcest.cn")
    req.add_header("Referer", "https://ysg.ckcest.cn/")
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

    print "hello"
    for i in range(1696, 2667):
        time.sleep(random.randint(2, 15))
        print 'i=' + str(i)
        result = get_content(i)
        # print 'result type='
        # print type(result)
        data = json.loads(json.loads(result).encode('utf-8'))
        # print 'data type='
        # print type(data)
        sqlList = [];
        for item in data['newsList']:
            print 'date='+str(item['title'])
            # print item['title']
            acInfos = item.get('acInfos')
            acInfoIdList = []
            acInfoNameList = []
            for acInfo in acInfos:
                if(acInfo!=None):
                    acInfoId = acInfo.get('acInfoId')
                    acInfoName = acInfo.get('acInfoName')
                    acInfoIdList.append(str(acInfoId))
                    acInfoNameList.append(acInfoName)
            # print 'reportDate=' + str(item.get('reportDate'))
            # 时间戳转日期时间格式1639411200000
            if(item.get('reportDate')!=None):
                reportDate2 = timestampToDate(int(item.get('reportDate')) / 1000)
            # print item['speciality']
            # %s字符串 %d整数 %f浮点数

            sql = "INSERT INTO scweb_compare.scindex_caeysg_ysdt( dataId, row_id, acInfoId, acInfoName, href, mediaName, reportDateAcc, title, cover, reportDate, reportDate2,recordTime,acInfos)  VALUES ('%s', '%s', '%s', '%s', '%s','%s', '%s', '%s','%s', '%s', '%s','%s','%s')" % (
                db.escape_string(str(noneToEmptyStr(item.get('id')))),
                db.escape_string(str(noneToEmptyStr(item.get('ROW_ID')))),
                db.escape_string(','.join(acInfoIdList)), db.escape_string(','.join(acInfoNameList)),
                db.escape_string(noneToEmptyStr(item.get('href'))),
                db.escape_string(noneToEmptyStr(item.get('mediaName'))),
                db.escape_string(str(noneToEmptyStr(item.get('reportDateAcc')))),
                db.escape_string(noneToEmptyStr(item.get('title'))),
                db.escape_string(noneToEmptyStr(item.get('cover'))),
                db.escape_string(str(noneToEmptyStr(item.get('reportDate')))),
                db.escape_string(noneToEmptyStr(reportDate2)),
                time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                db.escape_string(noneToEmptyStr(listToJsonStr(item.get('acInfos')))))
            sqlList.append(sql)
        #     每页sql执行完再更新数据库，方便断点续传
        try:
            for sql in sqlList:
                print 'sql='+sql
                cursor.execute(sql)
            db.commit()
            print "success"
        except Exception, e:
            db.rollback()
            db.close()
            print repr(e)
        # print result
