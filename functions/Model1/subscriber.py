# !/usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
import os
from time import sleep
import random
sys.path.append(os.path.dirname(__file__))

from monitor import RedisHelper
pwd = os.path.dirname(__file__)
father_path = os.path.abspath(os.path.dirname(pwd)+os.path.sep+".")
obj = RedisHelper()
redis_sub = obj.subscribe()

def isOpen(filename):
    p = os.popen("lsof %s" % filename)
    content = p.read()
    p.close()
    return bool(len(content))

def recive_msg():
    msg = redis_sub.parse_response()
    name, model = obj.getmodel()
    name = father_path+'/'+name
    model = bytearray(model)
    #time = random.random()*5  # 暂停时间
    #sleep(time)  # 休眠时间
    # 如果该文件没有被读写
    if isOpen(name) == False:
        print('正在写文件:'+name.split('/')[-1])
        f = open(name, 'wb')
        f.write(model)
        #sleep(20)  # 保证不重复写文件
        f.close()
    else:
        # 如果被打开则不停检查是否已经写完
        print('互斥锁:'+name.split('/')[-1])
        while True:
            if os.path.exists(name) == True:
                if isOpen(name) == False:
                    break
    print('写结束')
    if '.bin' not in name:
        return name, msg[2]
    else:
        return 0, msg[2]
