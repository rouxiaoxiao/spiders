# -*-coding:utf-8-*-
# import urllib
from evaluate import getTrainTest, evaluate


def itemPop(filename, topk):
    train, test = getTrainTest(filename)
    dict = {}
    i_set = set()
    i_dict = {}
    index = 0
    print "开始生成 物品交互次数排名 i_dict_sort"
    for train_line in train:
        index = index + 1
        if index % 10000 == 0:
            print "index=" + str(index)
        train_line_sub = train_line.split("::")
        uid = train_line_sub[0]
        iid = train_line_sub[1]
        i_set.add(iid)
        if dict.has_key(uid):
            dict_list = dict[uid]
            list2 = []
            for list_iid in dict_list:
                list2.append(list_iid)
            list2.append(iid)
            dict[uid] = list2
        else:
            dict_list = []
            dict_list.append(iid)
            dict[uid] = dict_list
        if i_dict.has_key(iid):
            i_dict[iid] = i_dict[iid] + 1
        else:
            i_dict[iid] = 1
    i_dict_sort = sorted(i_dict.items(), key=lambda d: d[1], reverse=True)
    print "结束生成 物品交互次数排名 i_dict_sort"
    test_dict = {}
    print "开始生成 test_dict"
    index = 0
    for test_line in test:
        index = index + 1
        if index % 1000 == 0:
            print "index=" + str(index)
        test_line_sub = test_line.split("::")
        uid = test_line_sub[0]
        iid = test_line_sub[1]
        i_set.add(iid)
        test_dict[uid] = iid
    print "结束生成 test_dict"
    i_list = list(i_set)
    tuijian_list_dict = {}
    print "开始生成 tuijian_list_dict"

    index = 0
    for test_uid in test_dict.keys():
        index = index + 1
        print "index=" + str(index)
        print "test_uid=" + str(test_uid)
        tuijian_list = []
        print "开始生成 unabserve_list"
        unabserve_list = [x for x in i_list if x not in dict[test_uid]]
        print "结束生成 unabserve_list"
        for i in range(len(i_dict_sort)):
            if i_dict_sort[i][0] in unabserve_list:
                tuijian_list.append(i_dict_sort[i][0])
            if len(tuijian_list) > topk - 1:
                break
        tuijian_list_dict[test_uid] = tuijian_list
    print "结束生成 tuijian_list_dict"
    print "train=" + str(len(train))
    print "test=" + str(len(test))
    print "test_dict=" + str(test_dict), "tuijian_list_dict" + str(tuijian_list_dict)
    return test_dict, tuijian_list_dict


if __name__ == '__main__':
    test_dict, tuijian_list_dict = itemPop("ml-1m")
    file = open("ml-1m/tmp.txt", 'a')
    file.write("test_dict=" + str(test_dict) + "\n" + "tuijian_list_dict" + str(tuijian_list_dict) + "\n")
    hr, ndcg = evaluate(test_dict, tuijian_list_dict, 10)
    print "hr=" + str(hr), "ndcg=" + str(ndcg)
    file.write("hr=" + str(hr) + "\n" + "ndcg=" + str(ndcg) + "\n")
    file.flush()
    file.close()

    # 测试代码
    # dict = {}
    # dict[1] = 6
    # dict[2] = 4
    # dict[9] = 5
    # dict_sort = sorted(dict.items(), key=lambda d: d[1], reverse=True)
    # print dict_sort
    # for i in range(10):
    #     print i
    # print dict_sort[0][0]
    # print dict_sort[0][1]

    # set=set()
    # set.add(1)
    # set.add(2)
    # set.add(1)
    # set.add(3)
    # list=list(set)
    # print list
