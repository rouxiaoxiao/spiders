文件说明
=========
ITjuzi                          IT桔子公司的相关信息<br>
    ITjuzi_spider.py                用于爬取IT橘子上60000+公司的信息，改动文件保存地址即可直接运行<br>
    putJsonTxt_to_MySQL.py          可把从网站（IT橘子等）爬取的json数据，保存在自己的MySQL数据库中<br>
58tongcheng                     58同城爬取<br>
JapDict                         日语词典的爬取<br>
Linkedln                        领英招聘信息的爬取<br>
StrokesGif                      汉字笔画的爬取<br>
TencentEDU                      腾讯课堂的爬取<br>
jiazhangbang                    家长帮的爬取<br>
ChinsesData                               汉字信息网站爬取<br>

技术说明
=========
python版本：python2.7   数据库类型：MySQL


更新日志
======
5.22 更新IT橘子爬虫内容，加入cookielib，改变了之前代码后来不能解析网页的错误，可以重新获取网页内容
     加入抛出异常语句，程序不会无故停止运行（但是不能同时开两个程序爬取，不然会报错）
     
     
     
