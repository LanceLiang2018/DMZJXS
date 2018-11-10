# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 00:18:25 2018

@author: fuwen

http://v2.api.dmzj.com/novel/${id}.json
"""

import requests,json,re,time

for BookId in range(1,9999):
    NovelUrl = 'http://v2.api.dmzj.com/novel/%d.json'%(BookId)
    NovelData = requests.get(NovelUrl).text
    if(len(NovelData)) > 100 :
        NovelData = NovelData.replace('<br>','')
        NovelJson = json.loads(NovelData)
        name = NovelJson['name']
        authors = NovelJson['authors']
        status = NovelJson['status']
        introduction = NovelJson['introduction']
        types = NovelJson['types'][0]
        CoverUrl = NovelJson['cover']
        with open('NovelList.txt','a',encoding='utf-8') as f:
            f.writelines(['%d —— %s(%s) —— %s\n'%(BookId,name,status,authors)])
            time.sleep(0.5)