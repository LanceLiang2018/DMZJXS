# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 00:08:34 2018

@author: fuwen

小说正文：
http://v2.api.dmzj.com/novel/download/${id}_${volume_id}_${chapter_id}.txt
http://v2.api.dmzj.com/novel/download/1629_9389_85470.txt
小说卷列表：
http://v2.api.dmzj.com/novel/chapter/${id}.json
http://v2.api.dmzj.com/novel/chapter/1629.json

合并电子书
copy *.txt 合并文件.txt
"""
import requests,json,re




No = 0
BookId = 1629
JuanUrl = 'http://v2.api.dmzj.com/novel/chapter/%d.json'%(BookId)
JuanData = requests.get(JuanUrl).content
JuanData = JuanData.decode('unicode_escape')
JuanJsons = json.loads(JuanData)

# 添加至目录
def add_to_catalog(catalog):
    with open('catalog.txt','a') as f:
        f.writelines([catalog,'\n\n'])

def add_to_markdowm(cont):
    with open('markdown.md','a') as g:
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
        #合并回车
        for i in range(5):
            text =text.replace('\r','\n')
            text =text.replace('\n\n','\n')
        text = text.replace('\n','\n\n')
        #删除markdown中的卷名、章节名
        Text = text.replace(volume_name,'')
        Text = Text.replace(chapter_name,'')
        add_to_markdowm(Text)
        with open(Chapter_name + '.txt','a') as f:
            f.writelines([text,'\n\n'])


