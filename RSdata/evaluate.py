# -*- Encoding:UTF-8 -*-
import heapq
import math

import numpy as np


def getTrainTest(filename):
    print "getTrainTest"
    if filename == "ml-1m":
        file = open("ml-1m/ratings.dat")
        print "file"
        train = []
        test = []
        index = 0
        pre_uid = -1
        for line in file:
            index = index + 1
            if index % 10000 == 0:
                print "运行到第" + str(index) + "行数据"
            lineSub = line.split("::")
            uid = lineSub[0]
            iid = lineSub[1]
            if uid != pre_uid:
                test.append(line)
            else:
                train.append(line)
            pre_uid = uid
        return train, test


def evaluate(test_dict, tuijian_dict, topK):
    def getHitRatio(ranklist, targetItem):
        for item in ranklist:
            if item == targetItem:
                return 1
        return 0

    def getNDCG(ranklist, targetItem):
        for i in range(len(ranklist)):
            item = ranklist[i]
            if item == targetItem:
                return math.log(2) / math.log(i + 2)
        return 0

    hr = []
    NDCG = []
    for test_uid in test_dict.keys():
        ranklist = tuijian_dict[test_uid][:topK]
        target_iid = test_dict[test_uid]
        tmp_hr = getHitRatio(ranklist, target_iid)
        tmp_NDCG = getNDCG(ranklist, target_iid)
        hr.append(tmp_hr)
        NDCG.append(tmp_NDCG)
    return np.mean(hr), np.mean(NDCG)


if __name__ == '__main__':
    test_dict = {'1': '2', '2': '3'}
    tuijian_dict = {'1': ['1', '2'], '2': ['1', '2']}
    hr, ndcg = evaluate(test_dict, tuijian_dict, 4)
    print "hr=" + str(hr)
    print "ndcg=" + str(ndcg)
