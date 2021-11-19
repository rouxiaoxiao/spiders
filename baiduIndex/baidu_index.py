# coding:utf-8

import requests


def decrypt(keys, data):
    # 解密函数
    half = len(keys) // 2
    pre = keys[:half]
    pro = keys[half:]
    dic = {pre[i]: pro[i] for i in range(half)}
    o = ''
    for d in data:
        try:
            o += str(dic[d])
        except Exception as e:
            pass
    # res=''.join([dict[d] for d in data])
    return o


def get_data(keyword, start_date, end_date):
    url_2 = 'http://index.baidu.com/Interface/ptbk?uniqid='
    url_1 = 'http://index.baidu.com/api/SearchApi/index?word=' + str(keyword) + '&area=0&startDate=' + str(
        start_date) + '&endDate=' + str(end_date)
    headers = {
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        # # 'cookie': 'BIDUPSID=3747C5BBD7B2A9991AE4FC98F38D321E; PSTM=1635905049; BAIDUID=3747C5BBD7B2A999B35DE2979CA403FF:FG=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; ab_jid=4d5d3fc5772bd391ba8a372ad0984606101c; ab_jid_BFESS=4d5d3fc5772bd391ba8a372ad0984606101c; __yjs_duid=1_8cfdcd917ddb18431b86229f284eed681635927618414; BDUSS=zM3SlUyWGFGSFMyMTVUb1VwbEdyZzk1Zm1KVUNVbmxaeH55bEVnbjI5ejhEYXRoRVFBQUFBJCQAAAAAAAAAAAEAAAAXOl4xyPjArXN1bW1lcgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPyAg2H8gINha; BDUSS_BFESS=zM3SlUyWGFGSFMyMTVUb1VwbEdyZzk1Zm1KVUNVbmxaeH55bEVnbjI5ejhEYXRoRVFBQUFBJCQAAAAAAAAAAAEAAAAXOl4xyPjArXN1bW1lcgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPyAg2H8gINha; BAIDUID_BFESS=3747C5BBD7B2A999B35DE2979CA403FF:FG=1; delPer=0; PSINO=1; H_PS_PSSID=34835_34885_34992_34067_34584_34504_34706_34917_34578_34812_26350_34826_34791; BA_HECTOR=al848kak0k0g8lak2c1go9l1c0r; BCLID=10745111021782746528; BDSFRCVID=JVDOJexroG0k-YnH7QFi-efUWrpWxY5TDYrELPfiaimDVu-VJeC6EG0Pts1-dEu-EHtdogKK0mOTHv-F_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tR30WJbHMTrDHJTg5DTjhPrM2tLJWMT-MTryKKJoHxT_OhjxyMAVbtKA3p5jLbvkJGnRh4oNBUJtjJjYhfO45DuZyxomtfQxtNRJQKDE5p5hKq5S5-OobUPUDMc9LUvqHmcdot5yBbc8eIna5hjkbfJBQttjQn3hfIkj2CKLtCD2MI_6DTt35n-WqxOK-PoJKCoMsJOOaCvPVCnOy4oTj6DlKb7BKpj70C38366H5f5RJMO53j-53MvB-fnyBjFfBjKq-noFBpDhf4-9Qft20hKbeMtjBbLLQNO3bb7jWhk2Dq72ybDVQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8EjHCDq-cX5ITOsJoq2RbhKROvhjRrDf0gyxoObtRxtI0LhRrd04L5866NbloRKR8i2butLU3k-eTrbnQVKRTVsMQGqqjkbfJBQttjQn3et4jbK4KE3lnMeb7TyU42hf47yhDL0q4Hb6b9BJcjfU5MSlcNLTjpQT8r5MDOK5OuJRLDoKPhtK0WbnO1hnofq4D_MfOtetJyaR30bpvvWJ5TMC_6qj-VQx4njNbw2Ir-5HTUWCnb5PoGShPCb6-K0n0TQ2c4QRTHtb6lXRFb3l02VboIe-t2ynQD0NKL5-RMW20jWl7mWPLVsxA45J7cM4IseboJLfT-0bc4KKJxbnLWeIJIjjCaePFHbMoOetjK2CntsJOOaCvkSlbOy4oWK441DM4LX467Ja6lB66H5f5Rq4J52huh3M04K4orQP50KC5LKUQaHxQkeq8CQft20b0yDecb0RLL3mbJ0n7jWhk2Dq72ybDVQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8IjH62btt_tJCe_C3P; BCLID_BFESS=10745111021782746528; BDSFRCVID_BFESS=JVDOJexroG0k-YnH7QFi-efUWrpWxY5TDYrELPfiaimDVu-VJeC6EG0Pts1-dEu-EHtdogKK0mOTHv-F_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=tR30WJbHMTrDHJTg5DTjhPrM2tLJWMT-MTryKKJoHxT_OhjxyMAVbtKA3p5jLbvkJGnRh4oNBUJtjJjYhfO45DuZyxomtfQxtNRJQKDE5p5hKq5S5-OobUPUDMc9LUvqHmcdot5yBbc8eIna5hjkbfJBQttjQn3hfIkj2CKLtCD2MI_6DTt35n-WqxOK-PoJKCoMsJOOaCvPVCnOy4oTj6DlKb7BKpj70C38366H5f5RJMO53j-53MvB-fnyBjFfBjKq-noFBpDhf4-9Qft20hKbeMtjBbLLQNO3bb7jWhk2Dq72ybDVQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8EjHCDq-cX5ITOsJoq2RbhKROvhjRrDf0gyxoObtRxtI0LhRrd04L5866NbloRKR8i2butLU3k-eTrbnQVKRTVsMQGqqjkbfJBQttjQn3et4jbK4KE3lnMeb7TyU42hf47yhDL0q4Hb6b9BJcjfU5MSlcNLTjpQT8r5MDOK5OuJRLDoKPhtK0WbnO1hnofq4D_MfOtetJyaR30bpvvWJ5TMC_6qj-VQx4njNbw2Ir-5HTUWCnb5PoGShPCb6-K0n0TQ2c4QRTHtb6lXRFb3l02VboIe-t2ynQD0NKL5-RMW20jWl7mWPLVsxA45J7cM4IseboJLfT-0bc4KKJxbnLWeIJIjjCaePFHbMoOetjK2CntsJOOaCvkSlbOy4oWK441DM4LX467Ja6lB66H5f5Rq4J52huh3M04K4orQP50KC5LKUQaHxQkeq8CQft20b0yDecb0RLL3mbJ0n7jWhk2Dq72ybDVQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8IjH62btt_tJCe_C3P; ab_bid=b19419cb8027e60ede8b7f24ec9a5a6470bd; ab_sr=1.0.1_OGQwM2MzZjQxYTE2MTI0ODA1MWU3M2E0ZGNjNjc0NzFlY2E5ZTBkNGM5OTBmMzdlNjIyZTgwNDI4YThlODg5OGMxZTJkM2JhNzdkOTg3MTRmMWViOWJlNzg2M2RkNDhmOWQ5NjQwMWRhMmViY2VkOGVmZjJjNTNjMTViNjE2OTRhZWJmZWQ5MTA3NWVmNzAxNzRkM2Q5NzdjNDdjNDdlZg==; __yjs_st=2_OWJmODNlNDU5OGYxOTAwM2RkMWNjNzg0ZDU2YWRhYzY0ZTQ0MmE2Mjk2Nzc4OTMwYTZlODIwNzZjYzY1MTFmNmVlYzIwZmM2NTI3YzI2Y2RiOGRmYzFjNGQ0ODdjZmE5YTgxMmM3NGYzYzQ4NGM1MjdkNmUwNWZiZDI2OTg2OGFmMGE3MmFhMmMzZTlmYTdkOGZiZTIwMzc5MGMwZDZlN2JhODA5ODgzOTY4MjVkMjlkYTAzYTUzMGFlY2UyZTJlM2VjOGNiNzdlODBiMjdjY2U3ZDVhMDJlNTU4OWRkM2IyYWVhYmNmYmEyN2U3MGQxNWQ4ZDlhYzU2MDllMjVmZl83XzQ2NjhhNDgy; bdindexid=chevgj6pimed5sha9at1n215u6; RT="z=1&dm=baidu.com&si=ojznuz1pedn&ss=kvm0qdvy&sl=2&tt=1nu&bcn=https://fclog.baidu.com/log/weirwood?type=perf&ld=1v2"'
        # # 补充自己的cookie
        # 'cookie': 'BDUSS=FWZ1FaMGJEaFVadklibmlFTXhJQU5SaUIyNlBDZXRpOGREREw3QjQxTXdCN0JoRVFBQUFBJCQAAAAAAAAAAAEAAAAXOl4xyPjArXN1bW1lcgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADB6iGEweohhbG'
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'BIDUPSID=A8A38EEC556F4B2B248B1FE20D7E271E; PSTM=1636334110; BAIDUID=A8A38EEC556F4B2B7BB0573EDF3CC507:FG=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDSFRCVID=OnAOJexroG0k-YnHih-R-efUWrpWxY5TDYrELPfiaimDVu-VJeC6EG0Pts1-dEu-EHtdogKK0mOTHv-F_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tR30WJbHMTrDHJTg5DTjhPrMXUTCWMT-MTryKKJoHxT_ObTdqqKVbtKA3p5jLbvkJGnRh4oNBUJtjJjYhfO45DuZyxomtfQxtNRJQKDE5p5hKq5S5-OobUPUDMc9LUvqHmcdot5yBbc8eIna5hjkbfJBQttjQn3hfIkj2CKLK-oj-D-RjT-23e; __yjs_duid=1_04e35b890a5b7a57aa2e97efbd12d64b1636334113926; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1636334116; BDUSS=FWZ1FaMGJEaFVadklibmlFTXhJQU5SaUIyNlBDZXRpOGREREw3QjQxTXdCN0JoRVFBQUFBJCQAAAAAAAAAAAEAAAAXOl4xyPjArXN1bW1lcgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADB6iGEweohhbG; BDUSS_BFESS=FWZ1FaMGJEaFVadklibmlFTXhJQU5SaUIyNlBDZXRpOGREREw3QjQxTXdCN0JoRVFBQUFBJCQAAAAAAAAAAAEAAAAXOl4xyPjArXN1bW1lcgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADB6iGEweohhbG; CHKFORREG=adafa63f8cee635f34329a99de0c6a20; bdindexid=27s7t7ii4ubqi6p99r48gfuie3; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1636334406; ab_sr=1.0.1_NzRjOTE0ZTkxNWExNTllMzIzZmRlMWQxN2ZkOTcwZmE5NGZhZDFiNTBhZmFhMGE1Yjg4OWQxOWZlNzEyMGFiNTU5MDE0Mjc3NDBkZDhmYjMwZmIzODRlYTc5MmIyMjM0NGVjYjBlNTI2ZWFhYWM2MGM0ZjMzMmIzOWNlZTliMDkzNTZiMWE2MGUxYTA5NzZkZWI3NmQzOTczMzI3Zjg5Yg==; H_PS_PSSID=34833_34886_34990_34068_35053_34584_34504_34705_34916_34606_26350_34970; delPer=0; PSINO=1; BDSFRCVID_BFESS=OnAOJexroG0k-YnHih-R-efUWrpWxY5TDYrELPfiaimDVu-VJeC6EG0Pts1-dEu-EHtdogKK0mOTHv-F_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=tR30WJbHMTrDHJTg5DTjhPrMXUTCWMT-MTryKKJoHxT_ObTdqqKVbtKA3p5jLbvkJGnRh4oNBUJtjJjYhfO45DuZyxomtfQxtNRJQKDE5p5hKq5S5-OobUPUDMc9LUvqHmcdot5yBbc8eIna5hjkbfJBQttjQn3hfIkj2CKLK-oj-D-RjT-23e; RT="sl=0&ss=kvpz97mk&tt=0&bcn=https://fclog.baidu.com/log/weirwood?type=perf&z=1&dm=baidu.com&si=i2hkghhklgi&ul=1xs0v"',
        'Host': 'index.baidu.com',
        'Referer': 'https://index.baidu.com/v2/main/index.html',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
    }
    res = requests.get(url_1, headers=headers)
    data = res.json().get('data')['userIndexes'][0]['all']['data']
    uniqid = res.json().get('data').get('uniqid')
    res2 = requests.get(url_2 + str(uniqid), headers=headers)
    keys = eval(res2.text)['data']
    # o=''
    # for i in decrypt(keys,data).split(','):
    # o+=str(i)+'\n'
    return decrypt(keys, data).split(',')


keyword_list = ['新冠肺炎', '武汉加油', '日本捐赠']

result_dict = {}
start_dates = ['2021-10-01']
end_dates = ['2021-10-03']
for keyword in keyword_list:
    o_all = []
    for i in range(len(end_dates)):
        sa = get_data(keyword, start_dates[i], end_dates[i])
        o_all += sa
        print(end_dates[i])
        time.sleep(2)
    result_dict[keyword] = o_all
    print('done', keyword)
