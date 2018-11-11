# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 00:08:34 2018

@author: fuwen

"""

import requests,json,re,os
from urllib import request

BasePath = 'C:/Users/fuwen/Desktop/'
os.chdir(BasePath)
No = 0
BookId = 2304  
NovelUrl = 'http://v2.api.dmzj.com/novel/%d.json'%(BookId)
NovelData = requests.get(NovelUrl).text
NovelData = NovelData.replace('<br>','')
NovelJson = json.loads(NovelData)
CoverUrl = NovelJson['cover']
BookName = NovelJson['name']

#创建目录
Path = BookName
isExists=os.path.exists(Path)
if not isExists:
    os.makedirs(Path)
os.chdir(BasePath + Path)

request.urlretrieve(CoverUrl,'封面.jpg') 
print('已下载封面！')

JuanUrl = 'http://v2.api.dmzj.com/novel/chapter/%d.json'%(BookId)
JuanData = requests.get(JuanUrl).content
JuanData = JuanData.decode('unicode_escape')
JuanData = JuanData.replace(chr(13), "")
JuanJsons = json.loads(JuanData)

# 添加至目录
def add_to_catalog(catalog):
    with open('catalog.txt','a',encoding = 'utf-8') as f:
        f.writelines([catalog,'\n\n'])

def add_to_markdowm(cont):
    with open(BookName + '.md','a',encoding = 'utf-8') as g:
        g.writelines([cont,'\n\n'])
        
        

for JuanJson in JuanJsons: 
    volume_id = JuanJson['volume_id']#卷ID
    volume_name = JuanJson['volume_name']#卷名
    add_to_markdowm('## '+volume_name)
    add_to_catalog(volume_name)
    chapters_lists = JuanJson['chapters']
    for chapter_list in chapters_lists:
        No+=1
        chapter_id = chapter_list['chapter_id']#章节ID
        chapter_name = chapter_list['chapter_name']#章节名
        add_to_markdowm('### '+chapter_name)
        add_to_catalog(chapter_name)
        Chapter_name = str(No).zfill(2) + volume_name + chapter_list['chapter_name']
        DownloadUrl = 'http://v2.api.dmzj.com/novel/download/%d_%d_%d.txt'%(BookId,volume_id,chapter_id)
        text = requests.get(DownloadUrl).text
        text = text.replace('<br />','')
        text = text.replace('<br/>','')
        text = text.replace('&nbsp;','')
        text = text.replace('&hellip;','')
        text = text.replace('&mdash;','')
        text = text.replace(chr(13),'\n')
        #合并回车
        for i in range(5):
            text =text.replace('\r','\n')
            text =text.replace('\n\n','\n')
        text = text.replace('\n','\n\n')
        #删除markdown中的卷名、章节名
        Text = text.replace(volume_name,'')
        Text = Text.replace(chapter_name,'')
        add_to_markdowm(Text)
        print('已下载 --- '+Chapter_name)
        with open(Chapter_name + '.txt','a',encoding = 'utf-8') as f:
            f.writelines([text,'\n\n'])


