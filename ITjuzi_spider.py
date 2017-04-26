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
    req = urllib2.Request(url)
    req.add_header("User-Agent", random_header)
    req.add_header("Host", "www.itjuzi.com")
    req.add_header("Referer", "http://www.itjuzi.com/")
    req.add_header("GET", url)
    contentfirst = urllib2.urlopen(req)

    if contentfirst.getcode() != 200:
        return None
    content = contentfirst.read().decode('utf-8')
    soup = BeautifulSoup(content, "lxml")

    company_name1 = soup.find('h1', class_='seo-important-title')
    company_name = company_name1.get_text().strip().replace(" ", "")
    if len(company_name) > 15:
        company_name = company_name[:15].strip()

    type1 = soup.find('span', class_='scope c-gray-aset')
    type = type1.get_text().strip().replace("\n", "-")
    area1 = soup.find('span', class_="loca c-gray-aset")
    area = area1.get_text().strip().replace("\n", "")
    link1 = soup.find('a', class_="weblink")
    link = link1.get_text().strip()
    # no_longer_exist = '404' in soup.find('title')
    # if no_longer_exist:
    #     pass
    print "name:", company_name, "\n"
    print "type:", type, "\n"
    print "area:", area, "\n"
    print "link:", link, "\n"

    companyInfo = {}

    companyInfo['id'] = num
    companyInfo['name'] = company_name
    companyInfo['type'] = type
    companyInfo['area'] = area
    companyInfo['link'] = link

    member1 = soup.find_all('span', class_='c')
    for singlemember in member1:
        member = singlemember.get_text().strip()
        print "member:",member

        companyInfo.setdefault("member", []).append(member)


    if soup.find('span', class_="date c-gray"):
        last_invest_time1 = soup.find('span', class_="date c-gray")
        last_invest_time = last_invest_time1.get_text().strip().replace("\n", "")
        round1 = soup.find('span', class_="round")
        round = round1.get_text().strip().replace("\n", "")
        money1 = soup.find('span', class_="finades")
        money = money1.get_text().strip().replace("\n", "")
        print "time:" + last_invest_time, "\n"
        print "round:" + round, "\n"
        print "money:" + money, "\n"

        companyInfo['last_invest_time'] = last_invest_time
        companyInfo['round'] = round
        companyInfo['money'] = money


        invest_org1 = soup.select('.list-round-v2 tr td:nth-of-type(4) a')
        if len(invest_org1) > 0:
            invest_org = invest_org1[0].get_text()
            invest_org = invest_org.encode('utf-8')
            print "company", invest_org, "\n",
            companyInfo['invest_org'] = invest_org


    # print companyInfo
    # company_file.write(str(num).encode("utf-8") + "\n")

    return json.dumps(companyInfo, company_file, encoding="UTF-8", ensure_ascii=False)

    # company_file.write(unicode(company_info) )


if __name__ == '__main__':

    company_file = open("C:\Users\zhengzhongwang\Desktop\company_file.txt", "w+")

    for num in range(907, 6000, 1):
        print "id:", num

        urll = "http://www.itjuzi.com/company/{}".format(num)
        company_file = open("C:\Users\zhengzhongwang\Desktop\company_file.txt", "a")

        # get_content(urll, headers)
        # print get_content(urll, headers)
        company_file.write(get_content(urll, headers)+"\n")

        howlong = [9, 10, 11, 12]
        time.sleep(random.choice(howlong))

        company_file.close()
    company_file.close()

