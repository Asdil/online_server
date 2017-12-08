# !/usr/bin/env python2
# -*- coding: utf-8 -*-
# sql="""
# select tree_id,point_id,item_id,item_content,answer,hint,remark,question_options,item_type
# from
# (select tree.subject,tree.name,tree.tree_id,
#     t1.name as name1,t2.name as name2,t3.name name3,t4.name as name4,
#     t1.point_id as pid1,t2.point_id as pid2,t3.point_id as pid3,t4.point_id as pid4
#     from knowledge_point_tree as t1 join knowledge_point_tree as t2
#     on t1.level = 1 and t2.level=2 and t2.pid = t1.point_id and t1.tree_id = t2.tree_id
#     join knowledge_point_tree as t3
#     on t2.level = 2 and t3.level=3 and t3.pid = t2.point_id and t2.tree_id = t3.tree_id
#     join knowledge_point_tree as t4
#     on t3.level = 3 and t4.level=4 and t4.pid = t3.point_id and t4.tree_id = t3.tree_id
#     join knowledge_tree as tree on tree.tree_id = t1.tree_id) as t1 join
# (select t1.point_id,t1.item_id,item_content,answer,hint,remark,question_options,item_type
#     from item_point as t1 join item as t2 on t1.item_id = t2.item_id
#     where t2.state=0 and t2.in_source=2) as t2 on t1.pid4 = t2.point_id
# where tree_id in (203)
# """


# sql="""
# select *
# from
# (
# select subject,t1.class,t1.tree_id,pid1,pid2,pid3,pid4,t1.name1,t1.name2,t1.name3,t1.name4,
# 	t2.item_id,item_content,answer,hint,remark,question_options,options,answers
# from
# (select tree.class,tree.subject,tree.name,tree.tree_id,
#     t1.name as name1,t2.name as name2,t3.name name3,t4.name as name4,
#     t1.point_id as pid1,t2.point_id as pid2,t3.point_id as pid3,t4.point_id as pid4
#     from knowledge_point_tree as t1 join knowledge_point_tree as t2
#     on t1.level = 1 and t2.level=2 and t2.pid = t1.point_id and t1.tree_id = t2.tree_id
#     join knowledge_point_tree as t3
#     on t2.level = 2 and t3.level=3 and t3.pid = t2.point_id and t2.tree_id = t3.tree_id
#     join knowledge_point_tree as t4
#     on t3.level = 3 and t4.level=4 and t4.pid = t3.point_id and t4.tree_id = t3.tree_id
#     join knowledge_tree as tree on tree.tree_id = t1.tree_id and tree.class=1) as t1 join
# (select t1.point_id,t1.item_id,item_content,answer,hint,remark,question_options,options,answers
#     from item_point as t1 join item as t2 on t1.item_id = t2.item_id
#     where t2.state=0 and t2.in_source=2) as t2 on t1.pid4 = t2.point_id
#
# union all
#
#
# select subject,class,tree_id,pid1,pid2,pid3,pid4,name1,name2,name3,name4,
# 	item_id,item_content,answer,hint,remark,question_options,options,answers
# from
# (select tree.class,tree.subject,tree.name,tree.tree_id,
#     t1.name as name1,t2.name as name2,t3.name name3,t4.name as name4,
#     t1.point_id as pid1,t2.point_id as pid2,t3.point_id as pid3,t4.point_id as pid4
#     from knowledge_point_tree as t1 join knowledge_point_tree as t2
#     on t1.level = 1 and t2.level=2 and t2.pid = t1.point_id and t1.tree_id = t2.tree_id
#     join knowledge_point_tree as t3
#     on t2.level = 2 and t3.level=3 and t3.pid = t2.point_id and t2.tree_id = t3.tree_id
#     join knowledge_point_tree as t4
#     on t3.level = 3 and t4.level=4 and t4.pid = t3.point_id and t4.tree_id = t3.tree_id
#     join knowledge_tree as tree on tree.tree_id = t1.tree_id and tree.class=2) as t1 join
# knowledge_point_relation as points_relation on t1.pid4 = points_relation.point_id join
# (select t1.point_id,t1.item_id,item_content,answer,hint,remark,question_options,options,answers
#     from item_point as t1 join item as t2 on t1.item_id = t2.item_id
#     where t2.state=0 and t2.in_source=2) as t2 on points_relation.base_point_id = t2.point_id
# ) t
# where tree_id=179
#
# """

#     sql="""
# select item_content
# from
# (select tree.subject,tree.name,tree.tree_id,
#     t1.name as name1,t2.name as name2,t3.name name3,t4.name as name4,
#     t1.point_id as pid1,t2.point_id as pid2,t3.point_id as pid3,t4.point_id as pid4
#     from knowledge_point_tree as t1 join knowledge_point_tree as t2
#     on t1.level = 1 and t2.level=2 and t2.pid = t1.point_id and t1.tree_id = t2.tree_id
#     join knowledge_point_tree as t3
#     on t2.level = 2 and t3.level=3 and t3.pid = t2.point_id and t2.tree_id = t3.tree_id
#     join knowledge_point_tree as t4
#     on t3.level = 3 and t4.level=4 and t4.pid = t3.point_id and t4.tree_id = t3.tree_id
#     join knowledge_tree as tree on tree.tree_id = t1.tree_id) as t1 join
# (select t1.point_id,t1.item_id,item_content,answer,hint,remark,question_options,item_type
#     from item_point as t1 join item as t2 on t1.item_id = t2.item_id
#     where t2.state=0 and t2.in_source=2) as t2 on t1.pid4 = t2.point_id
# where tree_id = {} and item_id = {}
# """.format(tree_id, item_id)



# import pandas as pd
# from functions.conf.config import Config
# con = Config()
# conn = con.get_matrix_slave_con()

# def read_from_sql(item_id):
#     sql = '''select item_content from item where item_id={}'''.format(item_id)
#     df = pd.read_sql(sql, conn)
#     return df['item_content'].values[0]

import pandas as pd
from functions.Base.matrixrequest import itemId2Text
def read_from_sql(item_id):
    if type(item_id) != type([]):
        item_id = [item_id]
    df = itemId2Text(item_id)['item_content'].values
    answer = itemId2Text(item_id)['answer'].values
    return df, answer


















