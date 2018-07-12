# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
import json

from bs4 import BeautifulSoup, NavigableString, Tag
import os


def xmlToJson(xmlStr, set):
    xmlStr = xmlStr.replace('<b>', "###b###").replace('</b>', "###/b###").replace('<i>', "###i###").replace('</i>',
                                                                                                            "###/i###").replace(
        '<author>', "###author###").replace('</author>', "###/author###").replace('<work>', "###work###").replace(
        '</work>', "###/work###")
    soup = BeautifulSoup(xmlStr, "lxml")
    # print(soup)
    wordData = {}
    # 词头
    wordHead = ""

    if soup.find('e'):
        wordHead = soup.find('e').get('name')
    else:
        return

    # 第一部分：hg部分
    if soup.find('hg'):
        hgObj = {}
        wordData['hg'] = hgObj
        hg = soup.find('hg')
        cx = []
        vgObj = {}
        word_list = []
        for child in hg.children:
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
            hgObj['posg'] = cx

        if hg.find('infg'):
            bx_list = []
            infg = hg.find('infg')
            for child in infg.children:
                # 消除AttributeError: 'NavigableString' object has no attribute 'get_text'
                if isinstance(child, NavigableString):
                    continue
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
                hgObj['infg'] = bx_list

        if hg.find('xrg'):
            xrgObj = {}
            xrgObj['xr'] = hg.find('xrg').find('xr').get_text()
            xrgObj['chn'] = hg.find('xrg').find('chn').get_text()
            hgObj['xr'] = xrgObj

    # 第二部分：sg部分
    if soup.find('sg'):
        sgObj = {}
        msDictObj_list = []
        sg = soup.find('sg')
        wordData['sg'] = sgObj
        # print("sg:" + str(sg))
        if sg.find('se2'):
            se2_list = sg.find_all('se2')
            for se2 in se2_list:
                msDict_list = se2.find_all("msdict")
                for msDict in msDict_list:
                    msDictObj = {}
                    for child in msDict:
                        if child.name == 'lg' or child.name == 'sj':
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
                            msDictObj['eg'] = egObj_list
                        #     ??没有多个释义的例句吗
                        elif child.name == "vg":
                            vgObj = {}
                            if child.find('v'):
                                vgObj['v'] = child.find('v').get_text()
                            if child.find('lg'):
                                vgObj['lg'], vgObj['chn'] = child.find('lg').stripped_strings
                            msDictObj['vg'] = vgObj
                        elif child.name == "infg":
                            infgObj_list = []
                            for childd in child.children:
                                # 消除AttributeError: 'NavigableString' object has no attribute 'get_text'
                                if isinstance(childd, NavigableString):
                                    continue
                                infg_child = {}
                                if (childd.name != None):
                                    if childd.name == "cm":
                                        infg_child[childd.name], infg_child[childd.chn.name] = childd.stripped_strings
                                    elif child.name == "lg":
                                        infg_child[childd.chn.name] = childd.find_all('chn')[-1].get_text()
                                        infg_child[child.name] = childd.get_text().replace(
                                            childd.find_all('chn')[-1].get_text(), "")
                                    else:
                                        infg_child[child.name] = childd.get_text()
                                        if childd.get('type') != None:
                                            infg_child[child.name + "_type"] = childd.get('type')
                                        else:
                                            infg_child[childd.name + "_type"] = ""
                                infgObj_list.append(infg_child)
                            msDictObj['infg'] = infgObj_list

                        elif child.name == "vg":
                            vgObj = {}
                            if child.find('v'):
                                vgObj['v'] = child.find('v').get_text()
                            if child.find('lg'):
                                vgObj['lg'], vgObj['chn'] = child.find('lg').stripped_strings
                            msDictObj['vg'] = vgObj
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
                            msDictObj['eg'] = egObj_list
            msDictObj_list.append(msDictObj)

        sgObj['sense'] = msDictObj_list

    # 详细的相关词模块
    if soup.find('subentryblock'):
        subEntryObj_list = []
        wordData['subEntry'] = subEntryObj_list
        subEntryBlock = soup.find('subentryblock')
        subEntry_list = subEntryBlock.find_all('subentry')
        for subEntry in subEntry_list:
            for child in subEntry.children:
                if child.name == "se1" or child.name == "se2":
                    print(wordHead + str(child))
            subEntryObj = {}
            subEntryObj_list.append(subEntryObj)
            l = subEntry.find('l').get_text()
            subEntryObj['l'] = l
            subEntry_cx_list = []
            subEntryObj['posg'] = subEntry_cx_list
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
                            msDictObj['eg'] = egObj_list
                    subEntry_msDict_list.append(msDictObj)

    # 图片等信息
    if soup.find('feature'):
        featureObj_list = []
        feature_list = soup.find_all('feature')
        for feature in feature_list:
            featureObj = {}
            featureObj['type'] = feature.get('type')
            featureObj_list.append(featureObj)
            imageObj_list = []
            listObj_list = []
            tableObj_list = []
            for child in feature.children:
                if child.name == "image":
                    imageObj_list.append(child.get('name'))
                    featureObj['image'] = imageObj_list
                elif child.name == "list":
                    item_list = child.find_all('item')
                    featureObj['list'] = listObj_list
                    for item in item_list:
                        print("item:" + str(item))
                        itemObj = {}
                        listObj_list.append(itemObj)
                        item_str = item.get_text()
                        item_childObj_list = []
                        for child in item:
                            print("child:" + str(child))
                            if isinstance(child, NavigableString):
                                continue
                            item_childObj = {}
                            item_childObj_list.append(item_childObj)
                            item_childObj[child.name] = child.get_text()
                            item_str = item_str.replace(child.get_text(), "")
                        itemObj['item'] = item_str
                        if len(item_childObj_list) > 0:
                            itemObj['eg'] = item_childObj_list
                elif child.name == "table":
                    row_list = child.find_all('row')
                    featureObj['table'] = tableObj_list
                    for row in row_list:
                        tableObj = {}
                        tableObj_list.append(tableObj)
                        rowObj_list = []
                        tableObj['row'] = rowObj_list
                        cell_list = row.find_all('cell')
                        for cell in cell_list:
                            rowObj_list.append(cell.get_text())

                print("child" + str(child) + wordHead)

        wordData['feature'] = featureObj_list

    wordData['wordHead'] = wordHead

    return json.dumps(wordData, encoding="UTF-8", ensure_ascii=False)
    # return wordHead
    # return set


if __name__ == '__main__':
    path = "C:\Users\liangxiaolx\Desktop\\niujin\dataIn"
    data_out_file = open("C:\Users\liangxiaolx\Desktop\\niujin\dataOut/jsonData.json", "wb+")
    files = os.listdir(path)
    s = []
    words = set()
    for file in files:
        if not os.path.isdir(file):
            f = open(path + "/" + file)
            # print(path + "/" + file)
            iter_f = iter(f)
            for line in iter_f:
                print(xmlToJson(line, words))
                if xmlToJson(line, words) != None:
                    # 得到set所用
                    # 将新新元素和老元素合并近set
                    # result_set = xmlToJson(line, words)
                    # words = (words | result_set)
                    # 得到结果所用
                    jsonStr = xmlToJson(line, words).replace("###b###", '<b>').replace("###/b###", '</b>').replace(
                        "###i###", '<i>').replace("###/i###", '</i>').replace("###author###", '<author>').replace(
                        "###/author###", '</author>').replace("###work###", '<work>').replace("###/work###", '</work>')
                    data_out_file.write(jsonStr + "\n")
                    data_out_file.flush()

    # 写所有词头set
    # for word in words:
    #     if word.find(',') == -1:
    #         data_out_file.write(word + "\n")
    #     else:
    #         word_split = word.split(',')
    #         for w in word_split:
    #             data_out_file.write(w + "\n")
    #     data_out_file.flush()
    data_out_file.close()

