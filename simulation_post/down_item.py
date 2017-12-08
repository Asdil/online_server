#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from conf.config import Config
import pandas as pd
import os

class Down_item_id():
    def __init__(self):
        self.__sql1 = """select subject,class,tree_id,pid1,pid2,pid3,pid4,name1,name2,name3,name4,
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
    where t2.state=0 and t2.in_source=2) as t2 on points_relation.base_point_id = t2.point_id
where tree_id ={0} limit 1000

"""
        self.__con = Config()
        self.__conn = self.__con.get_matrix_slave_con()
        self.pwd = os.path.dirname(__file__)
        self.father_path = os.path.abspath(os.path.dirname(self.pwd)+os.path.sep+".")

    def get_item_id(self, tree_id):
        sql = self.__sql1.format(tree_id)
        df = pd.read_sql(sql, self.__conn)
        df = df[['item_id']].values.tolist()
        ret = []
        for each in df:
            ret.append(each)
        return ret