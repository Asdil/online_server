#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from conf.config import Config
from sklearn.externals import joblib
import pandas as pd
import os
import datetime
import sys
sys.path.append("..")
tree_name = ['高中数学', '初中数学', '高中物理', '初中物理', '高中化学', '初中化学', '高中生物']

class Download():
    def __init__(self):
        # 初始化
        self.__sql1 = """
select subject,class,tree_id,pid1,pid2,pid3,pid4,name1,name2,name3,name4,
	item_id,item_content,answer,hint,remark,question_options,options,answers,teach_item_type,difficulty
from
(select tree.class,tree.subject,tree.name,tree.tree_id,
    t1.name as name1,t2.name as name2,t3.name name3,t4.name as name4,
    t1.point_id as pid1,t2.point_id as pid2,t3.point_id as pid3,t4.point_id as pid4
    from knowledge_point_tree as t1 join knowledge_point_tree as t2
    on t1.level = 1 and t2.level=2 and t2.pid = t1.point_id and t1.tree_id = t2.tree_id
    join knowledge_point_tree as t3
    on t2.level = 2 and t3.level=3 and t3.pid = t2.point_id and t2.tree_id = t3.tree_id
    join knowledge_point_tree as t4
    on t3.level = 3 and t4.level=4 and t4.pid = t3.point_id and t4.tree_id = t3.tree_id
    join knowledge_tree as tree on tree.tree_id = t1.tree_id and tree.class=3) as t1 join
knowledge_point_relation as points_relation on t1.pid4 = points_relation.point_id join
(select t1.point_id,t1.item_id,item_content,answer,hint,remark,question_options,options,answers,teach_item_type,difficulty
    from item_point as t1 join item as t2 on t1.item_id = t2.item_id
    where t2.state=0 and t2.in_source=2 and t1.last_update_time < '{1}') as t2 on points_relation.base_point_id = t2.point_id
where tree_id in {0}

"""
        # 增量
        self.__sql2 ="""
select subject,class,tree_id,pid1,pid2,pid3,pid4,name1,name2,name3,name4,
	item_id,item_content,answer,hint,remark,question_options,options,answers,teach_item_type,difficulty
from
(select tree.class,tree.subject,tree.name,tree.tree_id,
    t1.name as name1,t2.name as name2,t3.name name3,t4.name as name4,
    t1.point_id as pid1,t2.point_id as pid2,t3.point_id as pid3,t4.point_id as pid4
    from knowledge_point_tree as t1 join knowledge_point_tree as t2
    on t1.level = 1 and t2.level=2 and t2.pid = t1.point_id and t1.tree_id = t2.tree_id
    join knowledge_point_tree as t3
    on t2.level = 2 and t3.level=3 and t3.pid = t2.point_id and t2.tree_id = t3.tree_id
    join knowledge_point_tree as t4
    on t3.level = 3 and t4.level=4 and t4.pid = t3.point_id and t4.tree_id = t3.tree_id
    join knowledge_tree as tree on tree.tree_id = t1.tree_id and tree.class=3) as t1 join
knowledge_point_relation as points_relation on t1.pid4 = points_relation.point_id join
(select t1.point_id,t1.item_id,item_content,answer,hint,remark,question_options,options,answers,teach_item_type,difficulty
    from item_point as t1 join item as t2 on t1.item_id = t2.item_id
    where t2.state=0 and t2.in_source=2 and t1.last_update_time > '{1}' and t1.last_update_time < '{2}') as t2 on points_relation.base_point_id = t2.point_id
where tree_id in {0}
"""

        self.__sql3 = """
select tree_id, name from knowledge_tree where name like '%{0}%' and class = 3
"""
        self.__sql4 = """
select tree_id,pid4,item_id,item_content,answer,teach_item_type,difficulty
from
(select tree.class,tree.subject,tree.name,tree.tree_id,
    t1.name as name1,t2.name as name2,t3.name name3,t4.name as name4,
    t1.point_id as pid1,t2.point_id as pid2,t3.point_id as pid3,t4.point_id as pid4
    from knowledge_point_tree as t1 join knowledge_point_tree as t2
    on t1.level = 1 and t2.level=2 and t2.pid = t1.point_id and t1.tree_id = t2.tree_id
    join knowledge_point_tree as t3
    on t2.level = 2 and t3.level=3 and t3.pid = t2.point_id and t2.tree_id = t3.tree_id
    join knowledge_point_tree as t4
    on t3.level = 3 and t4.level=4 and t4.pid = t3.point_id and t4.tree_id = t3.tree_id
    join knowledge_tree as tree on tree.tree_id = t1.tree_id and tree.class=3) as t1 join
knowledge_point_relation as points_relation on t1.pid4 = points_relation.point_id join
(select t1.point_id,t1.item_id,item_content,answer,hint,remark,question_options,options,answers,teach_item_type,difficulty
    from item_point as t1 join item as t2 on t1.item_id = t2.item_id
    where t2.state=0 and t2.in_source=2) as t2 on points_relation.base_point_id = t2.point_id
where item_id in {0} and tree_id = {1}

"""

        self.__con = Config()
        self.__conn = self.__con.get_matrix_slave_con()
        self.pwd = os.path.dirname(__file__)
        self.father_path = os.path.abspath(os.path.dirname(self.pwd)+os.path.sep+".")

    def get_item(self, item_ids, tree_id):
        sql = self.__sql4.format('({0})'.format(','.join(item_ids)), tree_id)
        df = pd.read_sql(sql, self.__conn)
        return df

    def get_tree_id_df(self):
        flag = True
        for name in tree_name:
            sql = self.__sql3.format(name)
            df = pd.read_sql(sql, self.__conn)
            if flag:
                flag = False
                tree_id_df = df
            else:
                tree_id_df = [tree_id_df, df]
                tree_id_df = pd.concat(tree_id_df)
        return tree_id_df


    def get_tree_ids(self):
        #  ['高中数学', '初中数学', '高中物理', '初中物理', '高中化学', '初中化学', '高中生物']
        tree_id_df = self.get_tree_id_df()
        ret = {}
        for name in tree_name:
            df = tree_id_df[tree_id_df['name'].str.contains(u'{0}.*'.format(unicode(name, "utf-8")))]
            ret[name] = map(str, df['tree_id'].values.tolist())
        return ret

a = Download()
print a.get_tree_id_df()



