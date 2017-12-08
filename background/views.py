# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import datetime
father = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
from django.shortcuts import render
from models import Accury, Visit_record
# Create your views here.

# 更新后台


def upgrade_back(tree_id, lab, accury, md5):
    update_time = datetime.datetime.now()
    key = tree_id+lab
    try:
        obj = Accury.objects.get(key=key)
        obj.tree_id = tree_id
        obj.lab = lab
        obj.accury = accury
        obj.md5 = md5
        obj.update_time = update_time
        obj.save()
    except:
        obj = Accury(key=key, tree_id=tree_id, lab=lab, accury=accury,
                     md5=md5, pub_date=update_time, update_time=update_time)
        obj.save()


def upgrade_visitor(tree_id, item_id, result):
    pub_date = datetime.datetime.now()
    try:
        obj = Visit_record.objects.get(tree_id=tree_id, item_id=item_id)
    except:
        obj = Visit_record(tree_id=tree_id, item_id=item_id, result=result, pub_date=pub_date)
        obj.save()

