#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 12:03:42 2017

@author: root
"""
import json
import urllib2
import pandas as pd
from functions.conf.config import Config

class BaseRequests(object):
    #获取数据的基础请求方法
    @staticmethod
    def post_matrix(uri,params):
        HOST = Config.get_matrix_host()
        url = HOST + uri
        jdata = json.dumps(params)
        req = urllib2.Request(url)
        req.add_header('Content-Type','application/json')
        ret = urllib2.urlopen(req,jdata)
        return json.loads(ret.read())


def itemId2Text(item_ids):
    uri='item/query'
    '''
    params ={
        "app_id": "xbj",
        "app_key": "wenba",
        "item_ids": item_ids
    }
    '''
    params ={
        "app_id": "jiaoyan_points",
        "app_key": "1ea0cd699e8eec380",
        "item_ids": item_ids
    }   


    rs = BaseRequests.post_matrix(uri,params)
    try:
        df = pd.DataFrame.from_records(rs.get('items'))
        return df[[u"item_id",u"item_content",u"answer", \
                   u"hint",u"remark",u"question_options"]]
    except Exception,e:
        raise e

