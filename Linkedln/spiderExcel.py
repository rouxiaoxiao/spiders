# -*-coding:utf-8-*-
import urllib2
import random
import time
from bs4 import BeautifulSoup
import requests
import lxml
import re
import json
import sys
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


def get_content(url, headers):
    ''' @获取403禁止访问的网页 '''

    random_header = random.choice(headers)
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    req = urllib2.Request(url)
    # req.add_header("Cookie",
    #                "gr_user_id=56724441-ac89-45ac-b9cc-2e48d9ad7622; MEIQIA_EXTRA_TRACK_ID=3227266b1c39c4ab432a0c34d73b48b0; identity=18811778029%40test.com; remember_code=HCVU0bACu5; acw_tc=AQAAAC3ye31x6gQA7UZ+ewwQJCTHuYuL; session=d28a6d3a18c285268701b6099196df5fef26fd53; Hm_lvt_1c587ad486cdb6b962e94fc2002edf89=1493950205,1494402719,1494898661,1494990858; Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89=1494994080; _ga=GA1.2.1422503554.1492502104; _gid=GA1.2.2143681385.1494994080; acw_sc=591be879466cb8d61a76bebee7a7fd5bcff3619a")
    req.add_header("User-Agent", random_header)
    req.add_header("Host", "jobs.51job.com")
    req.add_header("Referer", "http://jobs.51job.com/")
    req.add_header("GET", url)
    # req.set_proxy()
    # contentfirst2 = urllib2.urlopen(req)
    try:
        contentfirst = opener.open(req)
        if contentfirst.getcode() != 200:
            return None
        # content = contentfirst.read().decode('utf-8')
        soup = BeautifulSoup(contentfirst, "lxml")
        positionInfo = {}
        # body > div.tCompanyPage > div.tCompany_center.clearfix > div.tHeader.tHjob > div > div.cn > h1
        if len(soup.select('div.tHeader.tHjob div h1'))>0:
            position = soup.select('div.tHeader.tHjob div h1')[0].get_text().replace(" ","").replace("\t","").replace("\n","").strip()
            positionInfo['position'] = position
        if soup.find('span',class_='lname'):
            address = soup.find('span',class_='lname').get_text().replace(" ","").replace("\t","").replace("\n","").strip()
            positionInfo['address'] = address
        if soup.find('p',class_='cname'):
            company = soup.find('p',class_='cname').get_text().replace(" ","").replace("\t","").replace("\n","").strip()
            positionInfo['company'] = company
        if soup.find('strong'):
            salary = soup.find('strong').get_text().replace(" ","").replace("\t","").replace("\n","").strip()
            positionInfo['salary'] = salary
        if soup.find('p',class_='msg ltype'):
            company_introduction = soup.find('p',class_='msg ltype').get_text().replace(" ","").replace("\t","").replace("\n","").strip()
            positionInfo['company_introduction'] = company_introduction
        if len(soup.find_all('span',class_='sp4'))>0:
            experience = soup.find_all('span',class_='sp4')[0].get_text().replace(" ","").replace("\t","").replace("\n","").strip()
            positionInfo['experience'] = experience
        if len(soup.find_all('span', class_='sp4')) > 1:
            education = soup.find_all('span',class_='sp4')[1].get_text().replace(" ","").replace("\t","").replace("\n","").strip()
            positionInfo['eduction'] = education
        if len(soup.find_all('span', class_='sp4')) > 2:
            number = soup.find_all('span', class_='sp4')[2].get_text().replace(" ","").replace("\t","").replace("\n","").strip()
            positionInfo['number'] = number
        if len(soup.find_all('span', class_='sp4')) > 3:
            release_time = soup.find_all('span', class_='sp4')[3].get_text().replace(" ","").replace("\t","").replace("\n","").strip()
            positionInfo['release_time'] = release_time
        if soup.find('div', class_='bmsg job_msg inbox'):
            description = soup.find('div', class_='bmsg job_msg inbox').get_text().replace(" ","").replace("\t","").replace("\n","").strip()
            positionInfo['description'] = description
        if len(soup.find_all('div', class_='tBorderTop_box'))>2:
            contact = soup.find_all('div', class_='tBorderTop_box')[2].get_text().replace(" ","").replace("\t","").replace("\n","").strip()
            positionInfo['contact'] = contact
        if len(soup.find_all('div', class_='tBorderTop_box'))>3:
            information1 = soup.find_all('div', class_='tBorderTop_box')[3]
            information = information1.get_text().replace(" ","").replace("\t","").replace("\n","").replace("\r","").strip()
            positionInfo['information'] = information

        positionInfo['id'] = num
        print num




        return json.dumps(positionInfo, position_file, encoding="UTF-8", ensure_ascii=False)

    except urllib2.URLError , e:
        print e.reason
        return None


def get_links(p):

    # html?lang = c & stype = & postchannel = 0000 & workyear = 99 & cotype = 99 & degreefrom = 99 & jobterm = 99 & companysize = 99 & providesalary = 99 & lonlat = 0 % 2C0 & radius = -1 & ord_field = 0 & confirmdate = 9 & fromType = & dibiaoid = 0 & address = & line = & specialarea = 00 &from= & welfare =

    url = "http://search.51job.com/list/000000,000000,0000,00,9,99,%25E4%25BA%25BA%25E5%25B7%25A5%25E6%2599%25BA%25E8%2583%25BD,2," + str(
        p) + ".html?"

    random_header = random.choice(headers)
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    req = urllib2.Request(url)
    # req.add_header("Cookie",
    #                "gr_user_id=56724441-ac89-45ac-b9cc-2e48d9ad7622; MEIQIA_EXTRA_TRACK_ID=3227266b1c39c4ab432a0c34d73b48b0; identity=18811778029%40test.com; remember_code=HCVU0bACu5; acw_tc=AQAAAC3ye31x6gQA7UZ+ewwQJCTHuYuL; session=d28a6d3a18c285268701b6099196df5fef26fd53; Hm_lvt_1c587ad486cdb6b962e94fc2002edf89=1493950205,1494402719,1494898661,1494990858; Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89=1494994080; _ga=GA1.2.1422503554.1492502104; _gid=GA1.2.2143681385.1494994080; acw_sc=591be879466cb8d61a76bebee7a7fd5bcff3619a")
    req.add_header("User-Agent", random_header)
    req.add_header("Host", "jobs.51job.com")
    req.add_header("Referer", "http://jobs.51job.com/")
    req.add_header("GET", url)

    try:
        contentfirst = opener.open(req)
        if contentfirst.getcode() != 200:
            return None

        soup = BeautifulSoup(contentfirst, "lxml")

        # resultList > div:nth-child(3) > p > span > a
        urls = soup.select("p span a")

        # for url in urls:
        #     url=url.get("href")
            # get_content(url,random_header)



        return urls

    except urllib2.URLError, e:
        print e.reason
        return None




if __name__ == '__main__':

    # company_file = open("C:/Users/xiaoxiao/Desktop/position_file.txt", "a")

    position_file = open("C:/Users/xiaoxiao/Desktop/rengong_file.txt", "a")
    random_header = random.choice(headers)
    num = 1
    for p in range(1,97,1):
        for url in get_links(p):
            url = url.get('href')
            get_content(url,random_header)
            if get_content(url, random_header) != None:
                try:

                    position_file.write(get_content(url, random_header)+'\n')
                    num = num+1
                except TypeError, a:
                    print a

            howlong = [1, 2, 3, 4]
            time.sleep(random.choice(howlong))

    position_file.close()






    # for num in range(334674098,334674100, 1):
    #     print "id:", num
    #
    #     urll = "http://jobs.51job.com/chengdu/76431865.html?s=01&t=0"
    #     position_file = open("C:/Users/xiaoxiao/Desktop/position_file.txt", "a")
    #     # print get_content(urll,headers)
    #     get_content(urll, headers)
    #     print get_content(urll, headers)
    #     if get_content(urll, headers)!=None:
    #         try:
    #             position_file.write(get_content(urll, headers))
    #         except TypeError ,a:
    #             print a
    #
    #
    #
    #
        # howlong = [8.5,8,8.7,9.2]
        # time.sleep(random.choice(howlong))
    #
    #     position_file.close()
    # position_file.close()

