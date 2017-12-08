#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division
import os
from functions.Update import download_local
from functions.Update import download_Tree
import datetime
from sklearn.externals import joblib
import pandas as pd
import json

father_path = os.path.abspath(os.path.dirname(os.getcwd())+os.path.sep+".")
print(father_path)

connect_1 = download_Tree.Download()
all_tree_dict = connect_1.get_tree_ids()
connect_2 = download_local.Download2()


def save_data():  # 保存所有记录的题,包含预测正确和预测错误的题,保存在/Data1中
    for subject, trees in all_tree_dict.items():
        for tree in trees:
            df = connect_2.get_item_tree(tree)
            if df.empty == False:
                pid4 = df['result'].values.tolist()
                _pid4 = []
                for each in pid4:
                    tmp = json.loads(each[1:-1])[u'point'][u'1st_possible'][u'id']
                    _pid4.append(int(tmp))
                items = df['item_id'].values.tolist()
                df2 = connect_1.get_item(items, tree)
                if df2.empty == False:
                    df2.loc[:, u'pre_pid4'] = pd.Series(data=_pid4)
                    joblib.dump(df2, os.getcwd() + '/functions/Data1/' + tree + '.pkl')


def read_record():  # 读取保存的访问记录pkl原题
    record_dict = {}
    acc_dict = {}
    # father_path = os.path.abspath(os.path.dirname(os.getcwd())+os.path.sep+".")
    dir = os.getcwd() + '/functions/Data1'
    list = os.listdir(dir)  # 列出文件夹下所有的目录与文件
    for i in range(0, len(list)):
        path = os.path.join(dir, list[i])
        if path[-4:] == '.pkl':
            data = joblib.load(path)
            total = len(data)
            data = data[data.pid4 != data.pre_pid4]
            wrong = len(data)
            record_dict[list[i].split('.')[0]] = data
            acc_dict[list[i].split('.')[0]] = [str((wrong/total)*100)+'%', str(total), str(wrong)]
    return record_dict, acc_dict


def dump_date():
    date = str(datetime.datetime.now().month) + '|' + str(datetime.datetime.now().day)
    joblib.dump(date, os.getcwd() + '/functions/Data1/' + 'date')

def check_date():
    try:
        date = joblib.load(os.getcwd() + '/functions/Data1/' + 'date')
        _date = str(datetime.datetime.now().month) + '|' + str(datetime.datetime.now().day)
        if date == _date:
            return '不需要更新'
        return '需要更新'
    except:
        return '无date数据'








