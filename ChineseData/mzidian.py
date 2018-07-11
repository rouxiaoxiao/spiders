# -*-coding:utf-8-*-
# import urllib
import random
import sys
import time
import urllib
import urllib2
import json
import re

from bs4 import BeautifulSoup, NavigableString

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


# https://mzidian.911cha.com/?q=好
def get_content(url_suffix, wordHead, headers):
    url = 'https://mzidian.911cha.com/' + url_suffix
    random_header = random.choice(headers)
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    req = urllib2.Request(url)
    req.add_header("User-Agent", random_header)
    req.add_header("Host", "mzidian.911cha.com")
    req.add_header("Referer", "https://mzidian.911cha.com/")
    req.add_header("GET", url)
    try:
        contentfirst = opener.open(req)
        if contentfirst.getcode() != 200:
            return None
        content = contentfirst.read().decode('utf-8')
        time.sleep(1)
        soup = BeautifulSoup(content, "lxml")
        ChineseWords = {}

        print("wordHead:" + wordHead)
        ChineseWords['wordHead'] = wordHead

        # 第一模块内容
        # 获取真实的class和假的class
        print("part one start.....")
        box1 = soup.find_all('div', class_="box")[1]

        basicData = {}
        false_class_code = ""
        real_class_code = ""
        box1_cont = box1.find('div', class_="cont")
        box1_ul = box1.find('ul', class_="tip")
        li_list = box1_ul.find_all("li")

        ChineseWords['basicData'] = basicData
        # 解析第一个box中的ul标签中的内容
        # ul模块对应的key value，这部分有很多假值，并提取对应的真class和假class
        for li in li_list:
            li_key = li.find("span").get_text()
            li_value = ""
            li_span_list = li.find_all("span")
            li_a_list = li.find_all("a")
            if len(li_span_list) > 1:
                li_value = (li_span_list[- 1]).get_text()
                if len(li_span_list) > 2:
                    false_class_code = li_span_list[1].get("class")
                    real_class_code = li_span_list[2].get("class")
            elif len(li_a_list) > 0:
                li_value = li_a_list[-1].get_text()
            basicData[li_key] = li_value

        # 笔顺模块，也存在真假值，所以需要判断
        real_bishun = box1_cont.find_all('span')[-1].get_text()

        # 从box1中移除ul，然后进行解析剩下的部分
        box1_cont.ul.extract()
        basic_data_raw = str(box1_cont.get_text())
        basic_data_raw_split = re.split("(繁体部首|简体部首|拼音|注音|部首|部外笔画|总笔画|异体字|五笔|郑码|结构|区位|笔顺|仓颉|四角|电码|统一码)", basic_data_raw)
        for i in range(1, len(basic_data_raw_split), 2):
            if i % 2 != 0:
                basicData[basic_data_raw_split[i]] = basic_data_raw_split[i + 1]
        if basicData.has_key("笔顺"):
            basicData["笔顺"] = real_bishun

        if basicData.has_key("异体字"):
            data_list = []
            yitizi_list = basicData.get("异体字").split(" ")
            for yitizi in yitizi_list:
                if yitizi == "":
                    continue
                data_list.append(yitizi)
            basicData['异体字'] = data_list
        if basicData.has_key("拼音"):
            data_list = []
            pinyin_list = basicData.get("拼音").split(" ")
            for pinyin in pinyin_list:
                if pinyin == "":
                    continue
                data_list.append(pinyin)
            basicData['拼音'] = data_list
        if basicData.has_key("注音"):
            data_list = []
            zhuyin_list = basicData.get("注音").split(" ")
            for zhuyin in zhuyin_list:
                if zhuyin == "":
                    continue
                data_list.append(zhuyin)
            basicData['注音'] = data_list

        print("part one end.....")

        # 第二模块“基本解释”部分

        print("part two start.....")

        # 根据模块匹配
        mbList = []
        ChineseWords['basicExplanation'] = mbList
        box2 = soup.find_all('div', class_="box")[2]
        if box2.find('div', class_="title") and box2.find('div', class_="title").get_text() == "基本解释":
            if box2.find("div", class_="cont").find("div", class_="mb") or box2.find("div", class_="cont").find("div",
                                                                                                                class_="mtb"):
                if box2.find("div", class_="cont").find("div", class_="mb"):
                    children_list = box2.find("div", class_="cont").find("div", class_="mb").children
                elif box2.find("div", class_="cont").find("div", class_="mtb"):
                    children_list = box2.find("div", class_="cont").find("div", class_="mtb").children
                print("false_class_code:" + str(false_class_code))
                print("real_class_code:" + str(real_class_code))
                children_list = list(children_list)
                for child in children_list:
                    if child.name == "h3":
                        mbPart = {}
                        mbList.append(mbPart)
                        dataList = []
                        mbPart['name'] = child.get_text()
                    elif child.name == "p":
                        if child.get("class") == false_class_code:
                            continue
                        mbPart['data'] = dataList
                        if mbPart['name'] != "UNICODE":
                            if mbPart.has_key('word'):
                                dataList.append(child.get_text())
                            else:
                                mbPart['word'] = child.get_text()
                        else:
                            dataList.append(child.get_text())

            # 移除box2中的div部分，直接对text解析
            box2_cont = box2.find('div', class_="cont")
            if box2.find("div", class_="cont").find("div", class_="mb"):
                box2_cont.find('div', class_="mb").extract()
            box2_children_list = box2_cont.children
            box2_children_list = list(box2_children_list)
            for child in box2_children_list:
                if child.name == "h3":
                    mbPart = {}
                    mbList.append(mbPart)
                    dataList = []
                    mbPart['name'] = child.get_text()
                elif child.name == "p":
                    if child.get("class") == false_class_code:
                        continue
                    mbPart['data'] = dataList
                    box2_p_a_list = child.find_all("a")
                    for box2_p_a in box2_p_a_list:
                        dataList.append(box2_p_a.get_text())
                    if len(box2_p_a_list) == 0:
                        dataList.append(child.get_text())

        print("part two end.....")

        # 第三模块“详细解释”部分（这部分不是每个汉字都有的，所以要判断一下）
        print("part three start.....")
        detailedExplanationlist = []
        box2 = soup.find_all('div', class_="box")[3]
        mbList = []
        ChineseWords['detailedExplanation'] = mbList

        if box2.find('div', class_="title") and box2.find('div', class_="title").get_text() == "详细解释":
            detailed_explanation_mb_list = box2.find_all('div', class_="mb")
            # 遍历mb（多音词）
            for detailed_explanation_mb in detailed_explanation_mb_list:
                detailed_explanation_mb_children_list = list(detailed_explanation_mb.children)
                for child in detailed_explanation_mb_children_list:
                    if child.get_text() == "":
                        continue
                    print("child:" + str(child))
                    if child.name == "h3":
                        mbPart = {}
                        mbList.append(mbPart)
                        dataList = []
                        mbPart['name'] = child.get_text()
                    elif child.name == "p":
                        if child.get("class") == false_class_code:
                            continue
                        mbPart['data'] = dataList
                        if mbPart['name'] == "词性变化" or mbPart['name'] == "基本词义":
                            if child.find("strong"):
                                dataObj = {}
                                dataList.append(dataObj)
                                dataObj['word'] = child.get_text()
                                sense_list = []
                                dataObj['sense'] = sense_list
                            # 有可能第一个模块中没有假信息，所以没有得到false_class_id
                            if not vars().has_key('dataObj'):
                                continue
                            elif dataObj.has_key('word') and ('cx' not in dataObj):
                                # vars().has_key('dataObj') and \
                                print(child)
                                if child.find("span", class_="pinyin"):
                                    dataObj['word'] = dataObj.get('word') + "(" + child.get_text().replace(" ", ")")
                                if child.get_text() == "":
                                    dataObj['cx'] = ""
                                else:
                                    if child.get_text()[0] == "〈":
                                        dataObj['cx'] = child.get_text()
                            else:
                                if child.get_text()[0] == '(':
                                    sense_obj = {}
                                    sense_list.append(sense_obj)
                                    sense_obj['jmsy'] = child.get_text()
                                    lj_list = []
                                    sense_obj['lj'] = lj_list
                                else:
                                    if vars().has_key('lj_list'):
                                        lj_list.append(child.get_text())
                                    else:
                                        sense_obj = {}
                                        # if vars().has_key('sense_list'):
                                        #     sense_list.append(sense_obj)
                                        sense_list.append(sense_obj)
                                        sense_obj['jmsy'] = child.get_text()
                                        lj_list = []
                                        sense_obj['lj'] = lj_list
                        else:
                            box2_p_a_list = child.find_all("a")
                            for box2_p_a in box2_p_a_list:
                                dataList.append(box2_p_a.get_text())
                            if len(box2_p_a_list) == 0:
                                dataList.append(child.get_text())

        print("part three end.....")

        # ChineseWords['detailedExplanation'] = detailedExplanationlist
        print("ChineseWords:" + json.dumps(ChineseWords, encoding="UTF-8", ensure_ascii=False))
        return json.dumps(ChineseWords, encoding="UTF-8", ensure_ascii=False)

    except urllib2.URLError, e:
        print e.reason


if __name__ == '__main__':
    print "hello"
    wordHead_file = open("C:\Users\liangxiaolx\Desktop\ChineseWord\mzidian\dataIn\\wordHead_update(40001-end).txt")
    word_des_file = open("C:\Users\liangxiaolx\Desktop\ChineseWord\mzidian\dataOut\ChineseWordDes.json", "a")
    i = 0
    # for line in wordHead_file:
    #     i = i + 1
    #     print('~~~~~我是第' + str(i) + '个单词~~~~~位于' + line.split("####")[2] + '~~~~~' + time.asctime(
    #         time.localtime(time.time())))
    #     wordHead = line.split("####")[0].replace("\n", "")
    #     url_suffix = line.split("####")[1].replace("\n", "")
    #     print("wordHead:" + wordHead)
    #     print("url_suffix:" + url_suffix)
    #     howlong = [0.1, 0.2, 0.3, 0.4]
    #     time.sleep(random.choice(howlong))
    #     if get_content(url_suffix, wordHead, headers) != None:
    #         try:
    #             word_des_file.write(get_content(url_suffix, wordHead, headers) + "\n")
    #             word_des_file.flush()
    #         except Exception, a:
    #             print a
    #             continue
    # word_des_file.close()
    # wordHead_file.close()

    url_suffix = "zi597d.html"
    get_content(url_suffix, "好", headers)
