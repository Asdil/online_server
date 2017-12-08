# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# Create your models here.
class Accury(models.Model):
    key = models.CharField(u'主键', max_length=255)
    tree_id = models.CharField(u'树编号', max_length=255)
    lab = models.CharField(u'类标签', max_length=255)
    accury = models.CharField(u'正确率', max_length=255)
    md5 = models.CharField(u'模型md5验证码', max_length=255)
    pub_date = models.DateTimeField(u'创建时间', auto_now_add=True, editable = True)
    update_time = models.DateTimeField(u'更新时间',auto_now=True, null=True)

    def __unicode__(self):# 在Python3中用 __str__ 代替 __unicode__
        return self.tree_id + ' ' + self.lab


class Visit_record(models.Model):
    tree_id = models.CharField(u'树编号', max_length=255)
    item_id = models.CharField(u'题目编号', max_length=255)
    result = models.CharField(u'预测结果', max_length=350)
    pub_date = models.DateTimeField(u'创建时间', auto_now_add=True, editable = True)

    def __unicode__(self):   # 在Python3中用 __str__ 代替 __unicode__
        return self.tree_id

