# -*- coding: utf-8 -*-

import math
from itertools import islice

from evaluate import getTrainTest, evaluate


class ItemBasedCF:
    def __init__(self, datafile=None, filename=None):
        self.filename = filename
        # self.datafile = datafile
        # self.readData()
        self.splitData(self.filename)

    def readData(self, datafile=None):
        self.datafile = datafile or self.datafile
        self.data = []
        file = open(self.datafile, 'r')
        for line in islice(file, 0, None):  # file.readlines():
            userid, itemid, record, _ = line.split('::')
            self.data.append((userid, itemid, float(record)))

    def splitData(self, filename):
        self.testdata = {}
        self.traindata = {}
        train, test = getTrainTest(filename)
        print "test list=" + str(test)
        print "开始录入train数据"
        for train_line in train:
            train_line_sub = train_line.split("::")
            uid = train_line_sub[0]
            iid = train_line_sub[1]
            rank = train_line_sub[2]
            self.traindata.setdefault(uid, {})
            self.traindata[uid][iid] = float(rank)
        print "结束录入train数据"
        print "开始录入test数据"
        self.test_dict = {}
        for test_line in test:
            test_line_sub = test_line.split("::")
            uid = test_line_sub[0]
            iid = test_line_sub[1]
            rank = test_line_sub[2]
            self.test_dict[uid] = iid
            self.testdata.setdefault(uid, {})
            self.testdata[uid][iid] = rank
        print "结束录入test数据"

    def ItemSimilarity(self, train=None):
        train = train or self.traindata
        self.itemSim = dict()
        item_user_count = dict()  # item_user_count{item: likeCount} the number of users who like the item
        count = dict()  # count{i:{j:value}} the number of users who both like item i and j
        for user, item in train.items():  # initialize the user_items{user: items}
            for i in item.keys():
                item_user_count.setdefault(i, 0)
                item_user_count[i] += 1
                count.setdefault(i, {})
                for j in item.keys():
                    if i == j:
                        continue
                    # count.setdefault(i, {})
                    count[i].setdefault(j, 0)
                    count[i][j] += 1
        for i, related_items in count.items():
            self.itemSim.setdefault(i, dict())
            for j, cuv in related_items.items():
                # print "cuv=" + str(cuv), "item_user_count[i]=" + str(item_user_count[i]), "item_user_count[j]=" + str(
                #     item_user_count[j])
                self.itemSim[i].setdefault(j, 0)
                self.itemSim[i][j] = cuv / math.sqrt(item_user_count[i] * item_user_count[j] * 1.0)

    def recommend(self, user, train=None, k=10, nitem=5):
        train = train or self.traindata
        rank = dict()
        ru = train.get(user, {})
        # 找出关于某个用户的评分的物品及评分
        for i, pi in ru.items():
            # 在该用户的物品评分列表中找出和该物品最相似的k个物品
            for j, wj in sorted(self.itemSim[i].items(), key=lambda x: x[1], reverse=True)[0:k]:
                # 如果相似物品已经被用户评分，则跳过
                if j in ru:
                    continue
                rank.setdefault(j, 0)
                rank[j] += pi * wj

        return dict(sorted(rank.items(), key=lambda x: x[1], reverse=True)[0:nitem])

    def testRecommend(self, user):
        rank = self.recommend(user, k=10, nitem=10)
        rank_sort = sorted(rank.items(), key=lambda x: x[1], reverse=True)
        # print str("rank_sort" + str(rank_sort))
        # for i, rvi in rank.items():
        #     items = self.traindata.get(user, {})
        #     record = items.get(i, 0)
        # print ("%5s: %.4f--%.4f" % (i, rvi, record))
        return rank_sort


if __name__ == "__main__":
    file = open("itemKNN.txt", "a")

    ibc = ItemBasedCF(filename='ml-1m')  # 初始化数据
    file.write("data=" + str(ibc.filename) + "\n")
    print "开始计算物品相似度"
    ibc.ItemSimilarity()  # 计算物品相似度矩阵
    print "结束计算物品相似度"
    tuijian_list_dict = {}
    index = 0
    for test_key in ibc.test_dict.keys():
        index = index + 1
        print "处理到第" + str(index) + "条测试数据"
        # print "test_uid=" + str(test_key)
        rank_sort = ibc.testRecommend(user=test_key)
        file.write("uid=" + str(test_key) + "   rank_sort=" + str(rank_sort) + "\n")
        file.flush()
        # print "rank_sort=" + str(rank_sort)
        if rank_sort != None:
            for rank_item in rank_sort:
                if tuijian_list_dict.has_key(test_key):
                    dict_list = tuijian_list_dict[test_key]
                    list2 = []
                    for list_iid in dict_list:
                        list2.append(list_iid)
                    list2.append(rank_item[0])
                    tuijian_list_dict[test_key] = list2
                else:
                    dict_list = []
                    dict_list.append(rank_item[0])
                    tuijian_list_dict[test_key] = dict_list
        else:
            print "rank None test_uid=" + str(test_key)
    print "tuijian_list_dict=" + str(tuijian_list_dict)
    hr, ndcg = evaluate(ibc.test_dict, tuijian_list_dict, 10)
    print "hr=" + str(hr), "ndcg=" + str(ndcg)

    file.write("tuijian_list=" + str(tuijian_list_dict) + "\n")
    file.write("hr=" + str(hr) + "ndcg=" + str(ndcg) + "\n")
    file.flush()
    file.close()
