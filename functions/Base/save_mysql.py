#coding=utf-8
import pymysql
import json
import datetime
conn= pymysql.connect(
        host='10.2.1.117',
        port=3306,
        user='wenba',
        passwd='Ib5mvmxbrIgsjjhcOhx7m39agrvPpxlr',
        db='questions',
        )
cur = conn.cursor()

#创建数据表
#cur.execute("create table student(id int ,name varchar(20),class varchar(30),age varchar(10))")

#插入一条数据
# cur.execute("insert into result values(1,'wwwwww')")


#修改查询条件的数据
#cur.execute("update student set class='3 year 1 class' where name = 'Tom'")

#删除查询条件的数据
#cur.execute("delete from student where age='9'")

# cur.close()
# conn.commit()
# conn.close()

def write_result(tree_id, item_id, content):
    content = json.dumps(content)
    create_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("insert into demon_off_line(tree_id, item_id, result, create_date) "
                "values({0}, {1}, '{2}', '{3}')".format(tree_id, item_id, content, create_date))
    conn.commit()
