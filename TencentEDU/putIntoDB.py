import MySQLdb
import json
import io
import sys
reload(sys)
sys.setdefaultencoding('utf-8')




f = io.open("10000-100146.txt",encoding="utf8")


for line in f:
    # line = line.decode('utf-8', 'ignore')
    #line= json.loads(line)
    print line
    line = json.loads(line)
    org_name = line['org_name'].decode("utf8")
    org_url = line['org_url'].decode("utf8")
    student = line['student'].decode("utf8")
    classification=line['classification'].decode("utf8")
    title = line['title'].decode("utf8")
    org_student_num = line['org_student_num']
    comment_num = line['comment_num']
    price = line['price']
    org_praise = line['org_praise']
    org_course_num = line['org_course_num']
    praise = line['praise']
    id = line['id']

    db = MySQLdb.connect("127.0.0.1", "root", "root", "course")

    cursor = db.cursor()
    db.set_character_set('utf8')
    # dbc.execute('SET NAMES utf8;')
    # dbc.execute('SET CHARACTER SET utf8;')
    # dbc.execute('SET character_set_connection=utf8;')

    # sql = "INSERT INTO COMPANY(LINK,AREA, LTYPE, ID, NAME)"+
	#          "VALUES ("+link+","+area+","+ltype+", "+name+","+lid+")"
    sql = "INSERT INTO course_info(id, title, classification, org_name, price, student,praise,comment_num,org_url,org_praise,org_student_num,org_course_num) VALUES ('%d', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s','%s','%s')" % (id, title, classification, org_name, price, student,praise,comment_num,org_url,org_praise,org_student_num,org_course_num)
    try:
        cursor.execute(sql)

        db.commit()
        print "success"
    except Exception, e:
        db.rollback()
        db.close()
        print repr(e)


f.close()

