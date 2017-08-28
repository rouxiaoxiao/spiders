# -*-coding:utf-8 -*-
import os
import random
from httplib import HTTPException
from telnetlib import EC
import MySQLdb
import thread
from DBUtils.PooledDB import PooledDB
import requests
import signal

import json
from selenium import webdriver
import time
from bs4 import BeautifulSoup

from multiprocessing import Pool
from selenium.common.exceptions import InvalidSelectorException

import sys

from selenium.webdriver.support.wait import WebDriverWait

reload(sys)
sys.setdefaultencoding('utf-8')


peonSource = PooledDB(
    MySQLdb,
    2,
    host="127.0.0.1",
    port=3306,
    db="course",
    user="root",
    passwd="root",
    charset="utf8"
)

def save(courseInfo):

    if 'org_name' in courseInfo.keys():
        org_name = courseInfo['org_name'].decode("utf8")

    if 'org_url' in courseInfo.keys():
        org_url = courseInfo['org_url'].decode("utf8")

    if 'student'in courseInfo.keys():
        student = courseInfo['student'].decode("utf8")

    if 'classification' in courseInfo.keys():
        classification=courseInfo['classification'].decode("utf8")

    if 'title' in courseInfo.keys():
        title = courseInfo['title'].decode("utf8")

    if 'org_student_num' in courseInfo.keys():
        org_student_num = courseInfo['org_student_num'].decode("utf8")

    if 'comment_num' in courseInfo.keys():
        comment_num = courseInfo['comment_num'].decode("utf8")

    if 'price' in courseInfo.keys():
        price = courseInfo['price'].decode("utf8")

    if 'org_praise' in courseInfo.keys():
        org_praise = courseInfo['org_praise'].decode("utf8")

    if 'org_course_num' in courseInfo.keys():
        org_course_num = courseInfo['org_course_num'].decode("utf8")

    if 'praise' in courseInfo.keys():
        praise = courseInfo['praise'].decode("utf8")

    id = courseInfo['id']

    sql = "INSERT INTO course_info(id, title, classification, org_name, price, student,praise,comment_num,org_url,org_praise,org_student_num,org_course_num) VALUES ('%d', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s','%s','%s')"
    # print sql % (id, title, classification, org_name, price, student,praise,comment_num,org_url,org_praise,org_student_num,org_course_num)
    connect = peonSource.connection(shareable=False)
    cursor = connect.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    try:
        cursor.execute(sql % (id, title, classification, org_name, price, student, praise, comment_num, org_url, org_praise, org_student_num, org_course_num))
        connect.commit()
        print 'insert seccess'
    except Exception, e:
        print 'insert failure'
        course_file = open("wrong_page.txt", "a")
        course_file.write(id + "\n")
        course_file.close()
        connect.rollback()
        connect.close()
        print repr(e)
    connect.close()




def get_content(num):

    print "id:", num
    print time.ctime()
    url = 'https://ke.qq.com/course/{}'.format(num)

    page = ''
    while page == '':
        try:
            page = requests.get(url, timeout=60)
        except:
            print "Connection refused by the server.."
            print "Let me sleep for 5 seconds"
            print "ZZzzzz..."
            time.sleep(5)
            print "Was a nice sleep, now let me continue..."
        continue
    soup = BeautifulSoup(page.text, 'lxml')

    if soup.find_all('div', class_='msg-text'):
        # time.sleep(1)
        print 'not Found'
        return

    try:
        driver = webdriver.PhantomJS()
        driver.get(url)
        time.sleep(0.2)

        driver.find_element_by_xpath('//*[@id="js_tab"]/h2[3]')

        if (driver.find_element_by_xpath('//*[@id="js_tab"]/h2[3]')):

            driver.find_element_by_xpath('//*[@id="js_tab"]/h2[3]').click() #找到‘学员评论’按钮并点击
        else:
            return None
        time.sleep(0.5)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        courseInfo = {}
        courseInfo['id'] = num

        if soup.select('span.title-main'):
            title = soup.select('span.title-main')
            title_text = title[0].get_text()
            courseInfo['title'] = title_text

        if soup.find_all('span', class_="line-item statistics-apply"):
            student = soup.find_all('span', class_="line-item statistics-apply")
            student_text = student[0].get_text().strip().replace(" ", "")
            courseInfo['student'] = student_text

        if soup.find_all('span', class_="line-item statistics-rate"):
            praise = soup.find_all('span', class_="line-item statistics-rate")
            praise_text = praise[0].get_text().strip().replace(" ", "")
            courseInfo['praise'] = praise_text

        if (soup.find_all('span', class_="price free")):
            price = soup.find_all('span', class_="price free")
            price_text = price[0].get_text().strip().replace(" ", "")
            courseInfo['price'] = price_text
        else:
            price = soup.find_all('span', class_="price")
            price_text = price[0].get_text().strip().replace(" ", "")
            courseInfo['price'] = price_text

        if soup.find_all('nav', class_="breadcrumb inner-center"):
            classification = soup.find_all('nav', class_="breadcrumb inner-center")
            classification_text = classification[0].get_text().replace(" ", " > ")
            courseInfo['classification'] = classification_text

        if soup.find_all('div', class_="f-rc-list filter-comment-rank js-f-rc-list"):
            comment_num = soup.find_all('div', class_="f-rc-list filter-comment-rank js-f-rc-list")
            comment_num_text = comment_num[0].get_text().strip().replace(" ", "")
            courseInfo['comment_num'] = comment_num_text

        if soup.find_all('div', class_='tt-cover-name'):
            org_name = soup.find_all('div', class_='tt-cover-name')
            org_name_text = org_name[0].get_text().strip().replace(" ", "")
            courseInfo['org_name'] = org_name_text

        if soup.find_all('span', class_="item-num"):
            org_praise = soup.find_all('span', class_="item-num")
            org_praise_text = org_praise[0].get_text().strip().replace(" ", "")
            courseInfo['org_praise'] = org_praise_text

        if soup.find_all('span', class_='item-num js-item-num'):
            org_course_num = soup.find_all('span', class_='item-num js-item-num')
            org_course_num_text = org_course_num[0].get('data-num')
            courseInfo['org_course_num'] = org_course_num_text

        if soup.find_all('span', class_='item-num js-item-num'):
            org_student_num = soup.find_all('span', class_='item-num js-item-num')
            org_student_num_text = org_student_num[1].get('data-num')
            courseInfo['org_student_num'] = org_student_num_text

        if soup.select(' div.tt-cover-url > a '):
            org_url = soup.select(' div.tt-cover-url > a ')
            org_url_text = org_url[0].get('href')
            courseInfo['org_url'] = org_url_text

        driver.quit()


        print courseInfo
        save(courseInfo)
    except :
        print 'cannot get content'
        return None

# def fuc_time(time_out, url, num, course_file):
#     # 此为函数超时控制，替换下面的test函数为可能出现未知错误死锁的函数
#     def handler(signum, frame):
#         raise AssertionError
#
#     try:
#         signal.signal(signal.SIGALRM, handler)
#         signal.alarm(time_out)  # time_out为超时时间
#         temp = get_content(url, num, course_file)  # 函数设置部分，如果未超时则正常返回数据
#         return temp
#     except AssertionError:
#         print "%d timeout" % num  # 超时则报错



def get_url(start,end):
    pool = Pool()
    for i in range(start, end):
        try:
            pool.apply_async(get_content, (i,))
        except HTTPException, b:
            print i
            print b
    pool.close()
    pool.join()

def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

if __name__ == '__main__':

    get_url(69245, 100000)



