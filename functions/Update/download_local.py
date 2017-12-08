#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from conf2.config import Config
import pandas as pd
import os

class Download2():
    def __init__(self):
        self.__sql1 = """
select * from background_visit_record where tree_id = {0}

"""
        self.__con = Config()
        self.__conn = self.__con.get_matrix_slave_con()
        self.pwd = os.path.dirname(__file__)
        self.father_path = os.path.abspath(os.path.dirname(self.pwd)+os.path.sep+".")

    def get_item_tree(self, tree_id):
        sql = self.__sql1.format(tree_id)
        df = pd.read_sql(sql, self.__conn)
        return df