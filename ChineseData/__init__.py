# -*-coding:utf-8-*-
import json
import re

if __name__ == '__main__':
    print("hello world")
    # s = "啊拼音ā á ǎ à a 注音ㄚ ㄚˊ ㄚˇ ㄚˋ ˙ㄚ 简体部首口部部外笔画7画总笔画10画繁体部首口部部外笔画8画总笔画11画异体字呵 嗄五笔KBSK仓颉RNLR郑码JYAJ四角5303061020结构左中右电码0759区位1601统一码663C554A笔顺一フ一フ一一一フ一一丨フ一フ丨一丨フ一丨"
    # sub = re.split("(注音|部首)", s)
    # print(json.dumps(sub, encoding="UTF-8", ensure_ascii=False))
    list = [1, 2, 3, 4]
    for i in range(0, 10):
        if i % 2 == 0:
            list = {}
        else:
            print(vars().has_key('list'))
