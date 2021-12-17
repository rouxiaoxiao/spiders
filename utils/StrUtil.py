# -*-coding:utf-8-*-
def noneToNull(str):
    if str==None:
        return 'null'
    else:
        return str

def noneToEmptyStr(str):
    if str==None:
        return ''
    else:
        return str

if __name__ == '__main__':
    str='                                            1957年                                        ~    1962年                                                                                哈尔滨医科大学 医学系    学士学位                                        ';
    print str.strip().replace(" ","")