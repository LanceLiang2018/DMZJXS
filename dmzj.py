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
import requests,json
No = 0
BookId = 1629
JuanUrl = 'http://v2.api.dmzj.com/novel/chapter/%d.json'%(BookId)
JuanData = requests.get(JuanUrl).content
JuanData = JuanData.decode('unicode_escape')
JuanJsons = json.loads(JuanData)

for JuanJson in JuanJsons: 
    volume_id = JuanJson['volume_id']
    volume_name = JuanJson['volume_name']
    chapters_lists = JuanJson['chapters']
    for chapter_list in chapters_lists:
        No+=1
        chapter_id = chapter_list['chapter_id']
        chapter_name = chapter_list['chapter_name']
        chapter_name = str(No).zfill(2) + volume_name + chapter_list['chapter_name']
        DownloadUrl = 'http://v2.api.dmzj.com/novel/download/%d_%d_%d.txt'%(BookId,volume_id,chapter_id)
        text = requests.get(DownloadUrl).text
        text = text.replace('<br />','')
        text = text.replace('<br/>','')
        text = text.replace('&nbsp;','')
        text = text.replace('&hellip;','')
        text = text.replace('&mdash;','')
        
        with open(chapter_name + '.txt','a') as f:
            f.write(text)
