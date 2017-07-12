import MySQLdb
import json
import io
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


db = MySQLdb.connect("localhost","root","root","test" )


cursor = db.cursor()

#
# cursor.execute("DROP TABLE IF EXISTS COMPANY")
#
#
# sql = """CREATE TABLE COMPANY (
#          LINK  CHAR(20) ,
#          AREA  CHAR(20),
#          LTYPE CHAR(20),
#          NAME CHAR(20),
#          ID INT )"""
#
# cursor.execute(sql)


# db.close()

f = io.open("1-314.txt",encoding="utf8")


for line in f:
    # line = line.decode('utf-8', 'ignore')
    #line= json.loads(line)
    print line
    line = json.loads(line)
    link=line['link']
    area=line['area'].decode("utf8")
    ltype=line['type'].decode("utf8")
    name=line['name'].decode("utf8")
    lid=line['id']
    if 'money' in line.keys():
        money = line['money']
    else:
        money = ""
    if 'round' in line.keys():
        round = line['round']
    else:
        round = ""
    if 'member' in line.keys():
        member = str(',').join(line['member'])

    else:
        member = ""
    if ('last_invest_time' in line.keys()):
        last_invest_time = line['last_invest_time']
    else:
        last_invest_time = ""
    if 'invest_org' in line.keys():
        invest_org = line['invest_org']
    else:
        invest_org = ""
    print member

    db = MySQLdb.connect("localhost","root","root","test" )

    cursor = db.cursor()
    db.set_character_set('utf8')
    # dbc.execute('SET NAMES utf8;')
    # dbc.execute('SET CHARACTER SET utf8;')
    # dbc.execute('SET character_set_connection=utf8;')

    # sql = "INSERT INTO COMPANY(LINK,AREA, LTYPE, ID, NAME)"+
	#          "VALUES ("+link+","+area+","+ltype+", "+name+","+lid+")"
    sql = "INSERT INTO COMPANY_INFO(LINK, AREA, TYPE, COMPANY_NAME, ID, LAST_INVEST_TIME,ROUNDS,MONEY,INVEST_ORG,MEMBER) VALUES ('%s', '%s', '%s', '%s', '%d', '%s', '%s','%s','%s','%s')" % (link,area,ltype,name,lid,last_invest_time,round,money,invest_org,member)
    try:
        cursor.execute(sql)

        db.commit()
        print "success"
    except Exception, e:
        db.rollback()
        db.close()
        print repr(e)


f.close()