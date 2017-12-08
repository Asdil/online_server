# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')  # 很重要不然不能显示中文
# sys.path.append('..')
from functions import main


from django.shortcuts import render
from django.views.decorators import csrf

# 接收POST请求数据
def server(request):
    ret = {}
    if request.POST:
        ret['result'] =  main.input(request.POST['input'])
    return render(request, "post.html", ret)


