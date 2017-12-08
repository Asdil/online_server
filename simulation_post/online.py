#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import httplib, urllib
import json
from down_item import Down_item_id


#定义一个要提交的数据数组(字典)
tree_id = 254
item_ids = Down_item_id().get_item_id(tree_id)

httpClient = None
for item_id in item_ids:
    print(item_id)
    data = {"tree_id": tree_id, "item_id": item_id}
    data = json.dumps(data)
    params = data
    httpClient = httplib.HTTPConnection("10.2.1.117", 8000, timeout=30)
    httpClient.request("POST", "/jiekou_list", params)
    response = httpClient.getresponse()
    print response.read()




