# -*-coding:utf-8-*-
# import urllib
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
def get_content(id, headers):
    url = "https://www.douban.com/group/people/{}/joins".format(id)
    random_header = random.choice(headers)
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    req = urllib2.Request(url)
    req.add_header("User-Agent", random_header)
    req.add_header("Host", "www.douban.com")
    req.add_header("Referer", "https://www.douban.com/")
    req.add_header("GET", url)
    try:
        contentfirst = opener.open(req)
        if contentfirst.getcode() != 200:
            return None
        content = contentfirst.read().decode('utf-8')
        time.sleep(1)
        soup = BeautifulSoup(content, "lxml")
        # print soup
        # <ul class="grid02 cf">
        # wordHead = soup.findAll('ul', class_="grid02 cf")
        # download_gif(id,gif)
        if soup.find('div', class_='group-list group-cards'):
            people_groups = soup.find('div', class_='group-list group-cards').find_all('li')
            # print people_groups
            i = 1
            for people_group in people_groups:
                print "第" + str(i) + "个小组"
                title_div = people_group.find('div', class_='info').find('div', class_='title').find('a')
                title = title_div['title']
                href = title_div['href']
                print title
                print href
                f = open('C://Users/xiaoxiao/Desktop/doubanxiaozu.txt', 'a')
                f.write(str(id) + '_' + str(i) + '####' + title + '####' + href + '\n')
                f.close()
                i = i + 1

    except urllib2.URLError, e:
        print e.reason


if __name__ == '__main__':
    print "hello"
    for num in range(15667, 10000000, 1):
        print "id:", num
        print(str(num) + time.asctime(time.localtime(time.time())))
        howlong = [0.1, 0.2, 0.3, 0.4]
        time.sleep(random.choice(howlong))
        get_content(num, headers)
