# -*-coding:utf-8 -*-
import random
import threading
from httplib import HTTPException

import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
import time
from bs4 import BeautifulSoup

from multiprocessing import Pool
from selenium.common.exceptions import InvalidSelectorException

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def get_content(url,num,course_file):
    page = ''
    while page == '':
        try:
            page = requests.get(url)
        except:
            print "Connection refused by the server.."
            print "Let me sleep for 5 seconds"
            print "ZZzzzz..."
            time.sleep(5)
            print "Was a nice sleep, now let me continue..."
        continue
    # wb_data = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')

    if soup.find_all('div', class_='msg-text'):
        # time.sleep(1)
        print 'not Found'
        return None


    driver = webdriver.PhantomJS()
    driver.get(url)
    time.sleep(0.2)


    try:
        driver.find_element_by_xpath('//*[@id="js_tab"]/h2[3]')

        if (driver.find_element_by_xpath('//*[@id="js_tab"]/h2[3]')):

            driver.find_element_by_xpath('//*[@id="js_tab"]/h2[3]').click() #找到‘学员评论’按钮并点击
        else:
            return None
        time.sleep(0.2)
        soup = BeautifulSoup(driver.page_source, "html.parser")


        title = soup.select('span.title-main')
        title_text = title[0].get_text()
        student = soup.find_all('span',class_="line-item statistics-apply")
        student_text = student[0].get_text().strip().replace(" ", "")
        praise = soup.find_all('span',class_="line-item statistics-rate")
        praise_text = praise[0].get_text().strip().replace(" ", "")
        if(soup.find_all('span',class_="price free")):
            price = soup.find_all('span',class_="price free");
            price_text = price[0].get_text().strip().replace(" ", "")
        else:
            price = soup.find_all('span',class_="price")
            price_text = price[0].get_text().strip().replace(" ", "")
        classification = soup.find_all('nav',class_="breadcrumb inner-center")
        classification_text = classification[0].get_text().replace(" ", " > ")
        comment_num = soup.find_all('div',class_ = "f-rc-list filter-comment-rank js-f-rc-list" )
        comment_num_text = comment_num[0].get_text().strip().replace(" ", "")
        org_name = soup.find_all('div',class_='tt-cover-name')
        org_name_text = org_name[0].get_text().strip().replace(" ", "")
        org_praise = soup.find_all('span',class_="item-num")
        org_praise_text = org_praise[0].get_text().strip().replace(" ", "")
        org_course_num = soup.find_all('span',class_='item-num js-item-num')
        org_course_num_text = org_course_num[0].get('data-num')
        org_student_num = soup.find_all('span',class_='item-num js-item-num')
        org_student_num_text = org_student_num[1].get('data-num')
        org_url = soup.select(' div.tt-cover-url > a ')
        org_url_text = org_url[0].get('href')

        courseInfo = {}
        courseInfo['id'] = num
        courseInfo['title'] = title_text
        courseInfo['student'] = student_text
        courseInfo['praise'] = praise_text
        courseInfo['price'] = price_text
        courseInfo['classification'] = classification_text
        courseInfo['comment_num'] = comment_num_text
        courseInfo['org_name'] = org_name_text
        courseInfo['org_praise'] = org_praise_text
        courseInfo['org_course_num'] = org_course_num_text
        courseInfo['org_student_num'] = org_student_num_text
        courseInfo['org_url'] = org_url_text

        driver.quit()

        return json.dumps(courseInfo, course_file, encoding="UTF-8", ensure_ascii=False)
    except:
        return None



def write_file(num):
    course_file = open("C:/Users/zhengzhongwang/Desktop/course_file_fast3.txt", "a")



    print "id:", num
    print time.localtime(time.time())
    url = 'https://ke.qq.com/course/{}'.format(num)
    if get_content(url,num,course_file) != None:
        try:
            course_file = open("C:/Users/zhengzhongwang/Desktop/course_file_fast3.txt", "a")
            course_file.write(get_content(url,num,course_file) + "\n")
            course_file.close()
            print get_content(url,num,course_file)
        except TypeError, a:
            print a
    else:
        print '404'


        # howlong = [                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         1,0.5,0.8]
        # time.sleep(random.choice(howlong))


    course_file.close()




def star(page):
    for num in range(1, 10000, 1):
        try:
            id = num + page
            write_file(id)
            time.sleep(0.01)
        except:
            continue

if __name__ == '__main__':
    ids = [110000, 120000, 130000, 140000, 150000, 160000, 170000, 180000, 190000]
    # http://jzb.com/bbs/thread-5988704-1-1.html
    threads = []
    for id in ids:
        t1 = threading.Thread(target=star, args=(id,))
        threads.append(t1)
        print "threads append success!"
    for t in threads:
        t.setDaemon(True)
        t.start()
        print "thread start"
    for t in threads:
        t.join()

