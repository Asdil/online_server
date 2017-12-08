# !/usr/bin/env python2
# -*- coding: utf-8 -*-
import os
# import logging
import pandas as pd
from shallowlearn.models import FastText
from apscheduler.scheduler import Scheduler
from Model1 import subscriber
import json
from functions.process.read_sql import read_from_sql
from process.washer import clear_words
from process.item_content_KNN5 import knn5
from Update import download_Tree
from log.hash import get_md5_02, update_log
# from Base.save_mysql import write_result
from background.views import upgrade_back, upgrade_visitor
from Base.princeple2 import my_principle
pwd = os.path.dirname(__file__)
father_path = os.path.abspath(os.path.dirname(pwd)+os.path.sep+".")
# logger = logging.getLogger("django") # 为loggers中定义的名称
# logger.info('开始服务')



# 定义模型池
class model_pool(object):
    tree_model = None
    # 面向item和diff
    itemdiff_trees = [9, 6, 4, 199, 164, 114, 209]
    itemdiff_name = {'高中数学':199,'初中数学':209,'高中生物':9,'初中化学':164,
                     '高中化学':6,'高中物理':4,'初中物理':144}
    # 面向pid4
    pid4_tree = download_Tree.Download()
    pid4_dict = pid4_tree.get_tree_ids()  # pid4 字典
    pid4_name = download_Tree.tree_name   # pin4 名字列表
    tree_id_change = {}
    for k, v in pid4_dict.items():
        for item in v:
            tree_id_change[int(item)] = itemdiff_name[k]

    dict_model = {}
    for tree_id in itemdiff_trees:
        dict_model[str(tree_id)+'pid4'] = None
        dict_model[str(tree_id)+'difficulty'] = None
    for _, trees in pid4_dict.items():
        for tree_id in trees:
            dict_model[str(tree_id)+'teach_item_type'] = None


    # 热启动使用,正常情况下是没有模型的
    @classmethod
    def hot_init(cls):
        cls.tree_model = FastText.load(pwd+'/Model1/alltree_id'+'.model')
        # 读取dif和item
        for tree_id in cls.itemdiff_trees:
            item = FastText.load(pwd+'/Model1/'+str(tree_id)+'teach_item_type'+'.model')
            dif = FastText.load(pwd+'/Model1/'+str(tree_id)+'difficulty'+'.model')
            cls.dict_model[str(tree_id)+'teach_item_type'] = item
            cls.dict_model[str(tree_id)+'difficulty'] = dif
        # 读取pid4
        for _, trees in cls.pid4_dict.items():
            for tree_id in trees:
                try:
                    pid4 = FastText.load(pwd+'/Model1/'+str(tree_id)+'pid4'+'.model')
                    cls.dict_model[str(tree_id)+'pid4'] = pid4
                except:
                    continue


    # 冷启动使用,更新数据
    @classmethod
    def updata_model(cls, name):
        if 'alltree_id' in name:
            cls.tree_model = FastText.load(name)
        else:
            _cor = name.split('/')[-1].split('.')[0]   # cls.dict_model在字典里的名字
            tmp = FastText.load(name)  # 加载模型
            cls.dict_model[_cor] = tmp  # 模型更新



# =============================
model_pool.hot_init()  # 测试热初始化
# =============================

sched = Scheduler()
@sched.interval_schedule(seconds=1)
def mytask():
    name, msg = subscriber.recive_msg()
    if name != 0:
        pass
        # logger.info(name.split('/')[-1]+"开始写入")
    else:
        # logger.info("bin文件开始写入")
        update_log("bin文件开始写入")
    if name != 0:
        model_pool.updata_model(name)
        # logger.info(name.split('/')[-1]+"更新完成" +'md5码:'+get_md5_02(name+'.CLF.bin'))
        update_log(name.split('/')[-1]+"更新完成" +'md5码:'+get_md5_02(name+'.CLF.bin'))
        if msg != None:
            msg = msg.split('|')
            # print msg[0], msg[1], msg[2]
            upgrade_back(msg[0], msg[1], msg[2], msg[3])

sched.start()

raw_df = pd.read_excel(pwd+'/pid4.xlsx')

dict1 = {0: '未知', 1:r'单选题', 2:r'填空题', 3:r'解答题', 4:r'实验题', 5:r'推断题', 6:r'计算题',
         7: r'多选题', 8:r'综合题', 9:r'判断题', 10:r'写作', 11:r'单词拼写', 12: r'句型转换',
         13: r'完型填空', 14:'改错题', 15: r'文言文阅读', 16:r'材料分析题'}
dict2 = {4: '物理', 16:'化学', 199:'数学',9:'生物'}
dict3 = {9: 8, 6: 5, 4: 4, 199: 2, 164: 5, 114: 4, 209: 2}  # subject[9, 6, 4, 199, 164, 114, 209]
# dict2 = {115104:r'第一节 正弦定理和余弦定理',
#          115105:r'第二节 应用举例',
#          115106:r'第一节 数列的概念与简单表示法',
#          115107:r'第二节 等差数列',
#          115108:r'第三节 等差数列的前n项和',
#          115109:r'第四节 等比数列',
#          115110:r'第五节 等比数列的前n项和',
#          115111:r'第一节 不等关系与不等式',
#          115112:r'第二节 一元二次不等式及其解法',
#          115113:r'第三节 二元一次不等式（组）与简单的线性规划问题',
#          115114:r'第四节 基本不等式'}

# /jiekou网址对应函数
# def input(words = None, tree_id = None, item_id = None):
#     # 内部使用单题, 有id号
#     if words != None:
#         words = clear_words(words)
#     # 判断学科
#     if tree_id == None:
#         if model_pool.tree_model == None:
#             return '没有树预测模型'
#         tree_id = int(model_pool.tree_model.predict([words])[0])
#
#     if tree_id != None and item_id != None:
#         words, _ = read_from_sql(int(item_id))[0]  # 默认单个语句
#         tree_id = int(tree_id)
#         words = clear_words(words)
#
#
#     # 从字典中加载模型
#     item = model_pool.dict_model[str(model_pool.tree_id_change[tree_id])+'teach_item_type']
#     pid4 = model_pool.dict_model[str(tree_id)+'pid4']
#     dif = model_pool.dict_model[str(model_pool.tree_id_change[tree_id])+'difficulty']
#     print '=================================='
#     print model_pool.tree_id_change[tree_id]
#     if item == None:
#         return '错误!没有item模型'
#     if pid4 == None:
#         return '错误!没有pid4模型'
#     if dif == None:
#         return '错误!没有dif模型'
#
#
#
#
#     teach_item_pros = []
#     teach_item_id = []
#     teach_item_name = []
#     predict = item._classifier.predict_proba(iter(' '.join(d) for d in [words]), item._label_count)
#     for i in range(3):
#         teach_item_pro = predict[0][i]
#         teach_item_id.append(str(teach_item_pro[0]))
#         teach_item_pros.append(str(teach_item_pro[1]*100))
#         teach_item_name.append(dict1[int(teach_item_pro[0])])
#
#
#
#     # pid4_id = int(pid4.predict([words])[0])
#     pid4_id = []
#     pid4_name = []
#     pid4_pros = []
#     predict = pid4._classifier.predict_proba(iter(' '.join(d) for d in [words]), pid4._label_count)
#     for i in range(3):
#         pid4_pro = predict[0][i]
#         pid4_id.append(str(pid4_pro[0]))
#         pid4_pros.append(str(pid4_pro[1]*100))
#         pid4_name.append(raw_df[raw_df['pid4'] == int(pid4_pro[0])]['name4'].values[0])
#
#
#
#
#     dif_id = int(dif.predict([words])[0])
#     result = {}
#     result['tree_id'] = tree_id
#     result['subject'] = dict3[tree_id]
#     result['dif'] = dif_id
#     result['point'] = {}
#     result['item_type'] = {}
#     protical = ['1st_possible', '2nd_possible', '3rd_possible']
#     for i in range(3):
#         result['point'][protical[i]] = {"id": str(pid4_id[i]), "name": str(pid4_name[i]), 'prob': str(pid4_pros[i])}
#     for i in range(3):
#         result["item_type"][protical[i]] = {"id": str(teach_item_id[i]), "name": str(teach_item_name[i]), 'prob': str(teach_item_pros[i])}
#
#     # result = {
#     #           'point': "id"+': '+str(pid4_id)+', '+"name"+': '+ str(pid4_name)+', '+'prob'+': '+str(pid4_pro),
#     #           "item_type": 'id'+': '+str(item_id)+', '+'name'+': '+str(item_name)+','+'prob'+': '+str(item_pro),}
#
#    # result = {'subject':dict2[tree_id],
#               #'point':{"id": str(pid4_id), "name": str(pid4_name), 'prob': str(pid4_pro)},
#               #"item_type": {'id': str(item_id), 'name': str(item_name), 'prob': str(item_pro)},
#               #'dif': str(dif_id)}
#     return result


# /jiekou_noid网址对应函数
# /jiekou_list网址对应函数
def input2(words = None, tree_id = None, item_id = None):
    # 多道题使用

    # words = r'<section class=\"stem\"><p>若函数<span class=\"latex\">\\(f(x)=(m-1)x^{2}+2mx+3\\)</span>是<span class=\"latex\">\\(R\\)</span>上的偶函数,则<span class=\"latex\">\\(f(-1)\\)</span>,<span class=\"latex\">\\(f(-\\sqrt{2})\\)</span>,<span class=\"latex\">\\(f(\\sqrt{3})\\)</span>的大小关系为（   ）</p><ul class=\"options\"><li><label class=\"option\">A:</label><span class=\"latex\">\\(f(\\sqrt{3})>f(-\\sqrt{2})>f(-1)\\)</span></li><li><label class=\"option\">B:</label><span class=\"latex\">\\(f(\\sqrt{3})< f(-\\sqrt{2})< f(-1)\\)</span></li><li><label class=\"option\">C:</label><span class=\"latex\">\\(f(-\\sqrt{2})< f(\\sqrt{3})< f(-1)\\)</span></li><li><label class=\"option\">D:</label><span class=\"latex\">\\(f(-1)< f(\\sqrt{3})< f(-\\sqrt{2})\\)</span></li></ul></section>'
    if words != None:
        words = [clear_words(words)]
        answers = [' ']
    # 判断学科
    if tree_id == None:
        if model_pool.tree_model == None:
            return '没有树预测模型'
        tree_id = int(model_pool.tree_model.predict([words])[0])

    if tree_id != None:
        # words, answers = read_from_sql(item_id)  # 此时有多道题
        # if len(words) != len(item_id):
        #     return 2
        tree_id = int(tree_id)
        new_words = []
        new_answer = []
        for i in range(len(words)):
            new_words.append(clear_words(words[i]))
            new_answer.append(clear_words(answers[i]))
    # item = model_pool.dict_model[str(tree_id)+'teach_item_type']
    pid4 = model_pool.dict_model[str(tree_id)+'pid4']
    dif = model_pool.dict_model[str(model_pool.tree_id_change[tree_id])+'difficulty']
    # if item == None:
    #     return '错误!没有item模型'
    if pid4 == None:
        return '错误!没有pid4模型'
    elif dif == None:
        return '错误!没有dif模型'

    # count = 0
    ret = []  # 返回数据
    for j in range(len(new_words)):
        word = new_words[j]
        answer = new_answer[j]
        tmp = my_principle(answer, 'teach_item_type')
        # if tmp != True:
        #     teach_item_pros = '99.99'
        #     teach_item_id = tmp
        # else:
        #     predict = item._classifier.predict_proba(iter(' '.join(d) for d in [word]), item._label_count)
        #     teach_item_pro = predict[0][0]
        #     teach_item_id = str(teach_item_pro[0])
        #     teach_item_pros = str(teach_item_pro[1]*100)

        pid4_id = []
        pid4_pros = []
        predict = pid4._classifier.predict_proba(iter(' '.join(d) for d in [word]), pid4._label_count)
        for i in range(3):
            pid4_pro = predict[0][i]
            pid4_id.append(str(pid4_pro[0]))
            pid4_pros.append(str(pid4_pro[1]*100))
        dif_id = int(dif.predict([word])[0])
        result = {}
        # result['item_id'] = int(item_id[j])
        result['subject'] = dict3[model_pool.tree_id_change[tree_id]]
        result['dif'] = dif_id
        result['point'] = {}
        # result['item_type'] = {}
        protical = ['1st_possible', '2nd_possible', '3rd_possible', 'knn_predict']
        if len(protical) > 2:
            for i in range(3):
                result['point'][protical[i]] = {"id": pid4_id[i], 'prob': pid4_pros[i]}
        else:
            for i in range(len(protical)):
                result['point'][protical[i]] = {"id": pid4_id[i], 'prob': pid4_pros[i]}
        result['point'][protical[3]] = {"id": knn5(5, new_words[0].replace(' ', ''))}

        # result["item_type"] = {"id": teach_item_id, 'prob': teach_item_pros}
        ret.append(result)
        # write_result(tree_id, item_id[count], result)
        # count += 1
    return ret


# /jiekou_list网址对应函数
def input3(words = None, tree_id = None, item_id = None):
    # 多道题使用
    if words != None:
        words = clear_words(words)
    # 判断学科
    if tree_id == None:
        if model_pool.tree_model == None:
            return '没有树预测模型'
        tree_id = int(model_pool.tree_model.predict([words])[0])

    if tree_id != None and item_id != None:
        words, answers = read_from_sql(item_id)  # 此时有多道题
        if len(words) != len(item_id):
            return 2
        tree_id = int(tree_id)
        new_words = []
        new_answer = []
        for i in range(len(words)):
            new_words.append(clear_words(words[i]))
            new_answer.append(clear_words(answers[i]))

    item = model_pool.dict_model[str(model_pool.tree_id_change[tree_id])+'teach_item_type']
    pid4 = model_pool.dict_model[str(tree_id)+'pid4']
    dif = model_pool.dict_model[str(model_pool.tree_id_change[tree_id])+'difficulty']



    if item == None:
        return '错误!没有item模型'
    elif pid4 == None:
        return '错误!没有pid4模型'
    elif dif == None:
        return '错误!没有dif模型'


    # count = 0
    ret = []  # 返回数据
    for j in range(len(new_words)):
        word = new_words[j]
        answer = new_answer[j]
        tmp = my_principle(answer, 'teach_item_type')
        if tmp != True:
            teach_item_pros = '99.99'
            teach_item_id = tmp
        else:
            predict = item._classifier.predict_proba(iter(' '.join(d) for d in [word]), item._label_count)
            teach_item_pro = predict[0][0]
            teach_item_id = str(teach_item_pro[0])
            teach_item_pros = str(teach_item_pro[1]*100)



        pid4_id = []
        pid4_pros = []
        predict = pid4._classifier.predict_proba(iter(' '.join(d) for d in [word]), pid4._label_count)
        for i in range(3):
            pid4_pro = predict[0][i]
            pid4_id.append(str(pid4_pro[0]))
            pid4_pros.append(str(pid4_pro[1]*100))


        dif_id = int(dif.predict([word])[0])

        result = {}
        result['item_id'] = int(item_id[j])

        result['subject'] = dict3[model_pool.tree_id_change[tree_id]]
        result['dif'] = dif_id
        result['point'] = {}
        result['item_type'] = {}
        protical = ['1st_possible', '2nd_possible', '3rd_possible', 'knn_predict']




        for i in range(3):
            result['point'][protical[i]] = {"id": pid4_id[i], 'prob': pid4_pros[i]}
        # print(new_words[0])
        # result['point'][protical[3]] = {"id": knn5(5, new_words[0].replace(' ', ''))}

        result["item_type"] = {"id": teach_item_id, 'prob': teach_item_pros}
        ret.append(result)
        # write_result(tree_id, item_id[count], result)
        # count += 1
        upgrade_visitor(str(tree_id), str(item_id[0]), json.dumps(ret))  # 将访问记录存储到sql

    return ret
