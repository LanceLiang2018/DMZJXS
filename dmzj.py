# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 00:08:34 2018

@author: fuwen

"""

import requests,json,re,os
from urllib import request

#配置
BookId = 1 
BasePath = 'C:/Users/fuwen/Desktop/'


os.chdir(BasePath)
No = 0
global Count
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

ImgPath = 'imgs'
isExists=os.path.exists(ImgPath)
if not isExists:
    os.makedirs(ImgPath)


TxtPath = 'TXT'
isExists=os.path.exists(TxtPath)
if not isExists:
    os.makedirs(TxtPath)

JuanUrl = 'http://v2.api.dmzj.com/novel/chapter/%d.json'%(BookId)
JuanData = requests.get(JuanUrl).content
JuanData = JuanData.decode('unicode_escape')
JuanData = JuanData.replace(chr(13), "")
JuanJsons = json.loads(JuanData)

# 添加至目录
def add_to_catalog(catalog):
    with open(TxtPath + '\\catalog.txt','a',encoding = 'utf-8') as f:
        f.writelines([catalog,'\n\n'])
# 目录添加至markdown文件
def add_to_markdowm(cont):
    with open(BookName + '.md','a',encoding = 'utf-8') as g:
        g.writelines([cont,'\n\n'])
# 内容添加至markdown文件        
def html_to_MD(text):
    Count = 0
    ImgCode = re.findall('<img.*/>',text)[0]
    text = text.replace(ImgCode,'')
    ImgUrls = re.findall('src="(.*?jpg)',ImgCode)
    for ImgUrl in ImgUrls:
        ImgName =  str(No) + '_' + str(Count) +'.jpg'
        download_pic(ImgUrl,ImgName)
        MD = '![](%s)\n\n' % (ImgPath + '/'+ImgName)
        text = text + MD
        Count+=1
    return text
# 下载图片
def download_pic(ImageUrl,ImgName):
    request.urlretrieve(ImageUrl,ImgPath + '\\'+ ImgName )
    print('图片%s下载已完成……'%ImgName)

# 文件名去特殊字符\/：*“<>|?
def ChangeFileName(filename):
    filename = filename.replace('\\','')
    filename = filename.replace('/','')
    filename = filename.replace('：','')
    filename = filename.replace('*','')
    filename = filename.replace('“','')
    filename = filename.replace('<','')
    filename = filename.replace('>','')
    filename = filename.replace('|','')
    filename = filename.replace('?','？')
    return filename

#下载封面
request.urlretrieve(CoverUrl,'cover.jpg')
print('封面已下载')

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
        try:
            Text = html_to_MD(Text)
        except Exception as e:
            pass
        
        add_to_markdowm(Text)
        print('已下载 --- ' + Chapter_name)
        Chapter_name = ChangeFileName(Chapter_name)
        with open(TxtPath + '\\'+ Chapter_name + '.txt','a',encoding = 'utf-8') as f:
            f.writelines([text,'\n\n'])


#pandoc下载
os.system('pandoc %s.md -o %s.epub --epub-cover-image=cover.jpg'%(BookName,BookName))
