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
    # "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    # "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    # "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    # "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    # "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    # "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    # "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    # "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    # "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    # "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    # "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    # "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    # "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    # "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    # "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    # "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    # "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    # "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    # "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    # "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    # "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    # "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    # "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    # "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    # "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    # "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    # "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    # "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    # "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    # "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    # "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    # "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    # "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    # "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
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
    req.add_header("Host", "www.itjuzi.com")
    req.add_header("Referer", "http://www.itjuzi.com/")
    req.add_header("GET", url)
    # req.set_proxy()
    # contentfirst2 = urllib2.urlopen(req)
    try:
        contentfirst = opener.open(req)
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
            print "member:", member

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

    except urllib2.URLError , e:
        print e.reason
        return None




    # company_file.write(unicode(company_info) )


if __name__ == '__main__':

    company_file = open("C:\Users\liangxiaolx\Desktop\companyTest.txt", "a")

    for num in range(43481, 50000, 1):
        print "id:", num

        urll = "http://www.itjuzi.com/company/{}".format(num)
        company_file = open("C:\Users\liangxiaolx\Desktop\companyTest.txt", "a")

        # get_content(urll, headers)
        # print get_content(urll, headers)
        if get_content(urll, headers)!=None:
            try:
                company_file.write(get_content(urll, headers)+"\n")
            except TypeError ,a:
                print a



        howlong = [8.5,8,8.7,9.2]
        time.sleep(random.choice(howlong))

        company_file.close()
    company_file.close()

