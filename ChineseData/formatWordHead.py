# -*-coding:utf-8-*-
import time

if __name__ == '__main__':
    wordHead_file = open("C:\Users\liangxiaolx\Desktop\ChineseWord\mzidian\dataIn\wordHead.txt")
    wordHead_update_file = open("C:\Users\liangxiaolx\Desktop\ChineseWord\mzidian\dataOut\wordHead_update.txt", "a")
    i = 1
    for line in wordHead_file:

        print('~~~~~我是第' + str(i) + '个单词~~~~~' + time.asctime(time.localtime(time.time())))
        wordHead = line.split("####")[0].replace("\n", "")
        url = line.split("####")[1].replace("\n", "")
        print("wordHead:" + wordHead)
        print("url:" + url)
        if line == "":
            continue
        if wordHead == "":
            continue
        wordHead_update_file.write(wordHead + "####" + url + "####" + str(i) + "\n")
        i = i + 1
    wordHead_update_file.close()
    wordHead_file.close()
