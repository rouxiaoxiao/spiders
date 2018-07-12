# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
import json

if __name__ == '__main__':

    data_out_file_in = open("C:\Users\liangxiaolx\Desktop\\niujin\dataOut/jsonData.json")
    data_out_file_merge = open("C:\Users\liangxiaolx\Desktop\\niujin\dataOut/jsonData_merge.json", "wb+")
    wordHead_set = set()
    result_map = dict()
    for line in data_out_file_in:
        value_list = []
        wordHead = json.loads(line)['wordHead']
        if result_map.has_key(wordHead):
            value_list.append(result_map[wordHead])
            value_list.append(json.loads(line))
        else:
            value_list.append(json.loads(line))
            result_map[wordHead] = value_list
        wordHead_set.add(wordHead)
    print(result_map)
    # for result in result_map:
    data_out_file_merge.write(json.dumps(result_map) + '\n')
    data_out_file_in.close()
    data_out_file_merge.close()
