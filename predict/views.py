# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import division
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from functions.process import background
from functions import main
from functions.Base.html_latex import show_latex
import json

type_str = type(str('string'))
# 错误时返回
def ret_error(ret):
    rs = {
        'ret': [],
        'msg': ret,
        'status_code': -1
    }
    rs = json.dumps(rs)
    return HttpResponse(rs)


# 成功时返回
def ret_success(ret):
    rs = {
        'ret': ret,
        'msg': 'success',
        'status_code': 0
    }
    rs = json.dumps(rs)
    return HttpResponse(rs)


# 其他未知错误时返回
def ret_unerro(e):
    rs = {
        'results': [],
        'msg': e.message,
        'status_code': -1
    }
    rs = json.dumps(rs)
    return HttpResponse(rs)


@csrf_exempt
def input(request):
    # 内部使用有id号
    try:
        # ret = request.GET['stem']
        if request.method == 'POST':
            ret = json.loads(request.body)
        stem = ret.get("stem", None)
        if stem == None:
            tree_id = ret.get("tree_id", None)
            item_id = ret.get("item_id", None)
            ret = main.input(tree_id=tree_id, item_id=item_id)
        else:
            ret = main.input(stem)
        print(ret, type(ret), type_str)
        # 如果返回错误
        if type(ret) == type_str:
            return ret_error(ret)
        # 成功时返回
        return ret_success(ret)
    except Exception, e:
        return ret_unerro(e)  # 未知错误返回

@csrf_exempt
def input2(request):
    # 外部使用,无id号
    try:
        # ret = request.GET['stem']
        if request.method == 'POST':
            ret = json.loads(request.body)
        stem = ret.get("stem", None)
        if stem == None:
            tree_id = ret.get("tree_id", None)
            item_id = ret.get("item_id", None)
            ret = main.input2(tree_id=tree_id, item_id=item_id)
        else:
            ret = main.input2(stem)
        # 如果返回错误
        if type(ret) == type_str:
            return ret_error(ret)
        return ret_success(ret)
    except Exception, e:
        return ret_unerro(e)

@csrf_exempt
def input3(request):
    #  多道题预测使用
    try:
        print request.body
        print(type(request.body))
        # ret = request.GET['stem']
        if request.method == 'POST':
            ret = json.loads(request.body)
        stem = ret.get("stem", None)
        if stem == None:
            tree_id = ret.get("tree_id", None)
            item_id = ret.get("item_id", None)
            ret = main.input3(tree_id=tree_id, item_id=item_id)
        else:
            ret = main.input(stem)
        # 如果返回错误
        if type(ret) == type_str:
            return ret_error(ret)
        return ret_success(ret)
    except Exception, e:
        return ret_unerro(e)




# for k, v in data.items():
#     print(v)
#     print('=====================================')
# print columns






def result(request):

    tmp = background.check_date()
    if tmp == '需要更新':
        background.save_data()
        background.dump_date()

    elif tmp == '无date数据':
        background.dump_date()
        background.save_data()


    data, acc_dict = background.read_record()

    for _, v in data.items():
        columns = v.columns.tolist()
        break
    for k, v in data.items():
        # tmp = v.values.tolist()
        # for i in range(len(tmp)):
        #     tmp[i][3] = show_latex(tmp[i][3])

        data[k] = v.values.tolist()
        tree_ids = data.keys()

    return render(request, 'item.html', {'data': data, 'tree_ids': tree_ids, 'columns': columns, 'acc_dict': acc_dict})


