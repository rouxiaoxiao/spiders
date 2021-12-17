# coding:utf-8
import time

# 时间戳到秒（毫秒级时间戳需要除1000）
def timestampToDate(timeStamp):
    if timeStamp==None:
        return ''
    # timeStamp = 1381419600
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


if __name__ == '__main__':
    print timestampToDate(1639411200000/1000)
    print timestampToDate(None)