# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
import json

from bs4 import BeautifulSoup, NavigableString, Tag
import os


def xmlToJson(xmlStr):
    soup = BeautifulSoup(xmlStr, "lxml")
    print(soup)
    wordData = {}
    # 词头
    wordHead = ""
    # 第一部分：基本信息
    hgObj = {}
    # 第二部分：详细信息
    sgObj = {}
    subEntryObj_list = []
    if soup.find('e'):
        wordHead = soup.find('e').get('name')
    else:
        return

    # 第一部分
    if soup.find('hg'):
        hg = soup.find('hg')
        cx = []
        vgObj = {}
        word_list = []
        for child in hg.children:
            print(child.get_text())
            if child.name == "hw":
                word = {}
                word_list.append(word)
                word['hw'] = child.get_text()
            elif child.name == "pr":
                ph_list = child.find_all('ph')
                phone_list = []
                for phone in ph_list:
                    phone_list.append(phone.get_text())
                word['phone'] = phone_list
            hgObj['word'] = word_list

        if hg.find('vg'):
            vg = hg.find('vg')
            if vg.find('v'):
                vgObj['v'] = vg.find('v').get_text()
            if vg.find('lg'):
                vgObj['lg'], vgObj['chn'] = vg.find('lg').stripped_strings
            hgObj['vg'] = vgObj

        if hg.find('posg'):
            posg = hg.find('posg')
            pos_list = posg.find_all('pos')
            for pos in pos_list:
                cx.append(pos.get('value'))
            hgObj['cx'] = cx

            if posg.find('infg'):
                bx_list = []
                infg = soup.find('infg')
                for child in infg.children:
                    # 消除AttributeError: 'NavigableString' object has no attribute 'get_text'
                    if isinstance(child, NavigableString):
                        continue
                    print(child)
                    infg_child = {}
                    if (child.name != None):
                        if child.name == "cm":
                            infg_child[child.name], infg_child[child.chn.name] = child.stripped_strings
                        elif child.name == "lg":
                            infg_child[child.chn.name] = child.find_all('chn')[-1].get_text()
                            infg_child[child.name] = child.get_text().replace(child.find_all('chn')[-1].get_text(), "")
                        else:
                            infg_child[child.name] = child.get_text()
                            if child.get('type') != None:
                                infg_child[child.name + "_type"] = child.get('type')
                            else:
                                infg_child[child.name + "_type"] = ""
                    bx_list.append(infg_child)
                    hgObj['bx'] = bx_list

        if hg.find('xrg'):
            xrgObj = {}
            xrgObj['xr'] = hg.find('xrg').find('xr').get_text()
            xrgObj['chn'] = hg.find('xrg').find('chn').get_text()
            hgObj['xr'] = xrgObj

    if soup.find('sg'):
        msDictObj_list = []
        sg = soup.find('sg')
        print("sg:" + str(sg))
        if sg.find('se2'):
            se2_list = sg.find_all('se2')
            for se2 in se2_list:
                msDict_list = se2.find_all("msdict")
                for msDict in msDict_list:
                    msDictObj = {}
                    for child in msDict:
                        if child.name == 'lg':
                            lgObj = {}
                            lgObj['lg'], lgObj['chn'] = child.stripped_strings
                            msDictObj['lg'] = lgObj
                        elif child.name == 'df':
                            dfObj = {}
                            dfObj['chn'] = child.find_all('chn')[-1].get_text()
                            dfObj['df'] = child.get_text().replace(child.find_all('chn')[-1].get_text(), "")
                            msDictObj['df'] = dfObj
                        elif child.name == "eg":
                            egObj_list = []
                            egObj = {}
                            egObj['chn'] = child.find_all('chn')[-1].get_text()
                            egObj['eg'] = child.get_text().replace(child.find_all('chn')[-1].get_text(), "")
                            if child.find("author"):
                                egObj['author'] = child.find("author").get_text()
                            if child.find('work'):
                                egObj['work'] = child.find("work").get_text()
                            egObj_list.append(egObj)

                            msDictObj['lj'] = egObj_list
                    msDictObj_list.append(msDictObj)

        elif sg.find('se1'):
            se1 = sg.find('se1')
            msDictObj = {}
            for child in se1:
                if child.name == 'lg':
                    lgObj = {}
                    lgObj['lg'], lgObj['chn'] = child.stripped_strings
                    msDictObj['lg'] = lgObj
                elif child.name == 'msdict':
                    for childd in child.children:
                        if childd.name == 'df':
                            dfObj = {}
                            dfObj['chn'] = childd.find_all('chn')[-1].get_text()
                            dfObj['df'] = childd.get_text().replace(childd.find_all('chn')[-1].get_text(), "")
                            msDictObj['df'] = dfObj
                        elif childd.name == "eg":
                            egObj_list = []
                            egObj = {}
                            author = ""
                            work = ""
                            if child.find("author"):
                                author = child.find("author").get_text()
                                egObj['author'] = author
                            if child.find('work'):
                                work = child.find("work").get_text()
                                egObj['work'] = work
                            egObj['chn'] = childd.find_all('chn')[-1].get_text()
                            egObj['eg'] = childd.get_text().replace(childd.find_all('chn')[-1].get_text(), "").replace(
                                author, "").replace(work, "")
                            egObj_list.append(egObj)
                            msDictObj['lj'] = egObj_list
            msDictObj_list.append(msDictObj)

        sgObj['sense'] = msDictObj_list

    # 详细的相关词模块
    if soup.find('subentryblock'):
        subEntryBlock = soup.find('subentryblock')
        subEntry_list = subEntryBlock.find_all('subentry')
        for subEntry in subEntry_list:
            subEntryObj = {}
            subEntryObj_list.append(subEntryObj)
            l = subEntry.find('l').get_text()
            subEntryObj['l'] = l
            subEntry_cx_list = []
            subEntryObj['cx'] = subEntry_cx_list
            subEntry_msDict_list = []
            subEntryObj['sense'] = subEntry_msDict_list
            if subEntry.find('posg'):
                subEntry_pos_list = subEntry.find_all('pos')
                for pos in subEntry_pos_list:
                    subEntry_cx_list.append(pos.get('value'))
            if subEntry.find('msdict'):
                msDict_list = subEntry.find_all("msdict")
                for msDict in msDict_list:
                    msDictObj = {}
                    for child in msDict:
                        if child.name == 'lg':
                            lgObj = {}
                            lgObj['lg'], lgObj['chn'] = child.stripped_strings
                            msDictObj['lg'] = lgObj
                        elif child.name == 'df':
                            dfObj = {}
                            dfObj['chn'] = child.find_all('chn')[-1].get_text()
                            dfObj['df'] = child.get_text().replace(child.find_all('chn')[-1].get_text(), "")
                            msDictObj['df'] = dfObj
                        elif child.name == "eg":
                            egObj_list = []
                            egObj = {}
                            egObj['chn'] = child.find_all('chn')[-1].get_text()
                            egObj['eg'] = child.get_text().replace(child.find_all('chn')[-1].get_text(), "")
                            if child.find("author"):
                                egObj['author'] = child.find("author").get_text()
                            if child.find('work'):
                                egObj['work'] = child.find("work").get_text()
                            egObj_list.append(egObj)
                            msDictObj['lj'] = egObj_list
                    subEntry_msDict_list.append(msDictObj)

    wordData['wordHead'] = wordHead
    wordData['hg'] = hgObj
    wordData['sg'] = sgObj
    wordData['subEntry'] = subEntryObj_list

    return json.dumps(wordData, encoding="UTF-8", ensure_ascii=False)


if __name__ == '__main__':
    path = "C:\Users\liangxiaolx\Desktop\\niujin\dataIn"
    data_out_file = open("C:\Users\liangxiaolx\Desktop\\niujin\dataOut/wordHead.json", "wb+")
    files = os.listdir(path)
    s = []
    for file in files:
        if not os.path.isdir(file):
            f = open(path + "/" + file)
            iter_f = iter(f)
            for line in iter_f:
                print(xmlToJson(line))
                if xmlToJson(line) != None:
                    jsonStr = xmlToJson(line)
                    data_out_file.write(jsonStr + "\n")
                    data_out_file.flush()
    data_out_file.close()
