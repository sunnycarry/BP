# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 11:47:07 2020

@author: SCPC
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pypinyin import pinyin,lazy_pinyin,Style
import jieba
import jieba.posseg as pseg
import json
import re

'''
data = {}
data["哈囉"] = []
data["哈囉"].append({"abc":"111"})
data["我"] = "n"
data["v"] = []
data["v"].append("吃")
data["v"].append("跑步")

with open('type.txt','r') as typefile:
    types = typefile.read().splitlines()
    for t in types:
        print(t)
    typefile.close()

with open('data.txt','w') as outfile:
    json.dump(data,outfile,ensure_ascii=False,)
outfile.close()

with open("type.txt",'a+') as typefile:
    typefile.write("v"+"\n")
    typefile.write("n"+"\n")
typefile.close()
'''

class_name = 'ipQwMb ekueJc RD0gLb'
url = 'https://news.google.com/topstories?hl=zh-TW&gl=TW&ceid=TW:zh-Hant'
remove_sign = ['\n',' ','','\r',', ',' ,']

def GetWebSourceTitle():
    r = requests.get(url)
    web_content = r.text
    soup = BeautifulSoup(web_content,'lxml')
    title = soup.find_all('h3',class_= class_name)
    return title

def GetNewsUrl(title):
    refs = [t.find('a')['href'].replace(".","https://news.google.com") for t in title]
    urls = [requests.get(t).url for t in refs]
    print("--------------------------------------")
    print(urls)
    return urls

def GetNewsTitleText(title):
    print("--------------------------------------")
    titles = [t.find('a').text for t in title]
    print(titles)
    return titles

def GetNewsArticleText(url):
    r = requests.get(url)
    content = r.text
    soup = BeautifulSoup(content,'lxml')
    articles = soup.find_all("p")
    article = []
    for a in articles:
        article.append(a.text)
    #article = [a for a in article for r in remove_sign if a != r ]
    strlist = []
    for a in article:
        print(a)
        sentences = re.split(r"[、，,。.（）：:」©!！.@?？\-─「．◎」》\[\]※\/►\s+]",a)
        for sentence in sentences:
            strlist.append(sentence)
    print(strlist)
    return strlist

def GetTone(word):
    tones = pinyin(word,style = Style.TONE3)
    t = []
    for tone in tones:
        t.append(tone[0][-1])
    return t

def CheckTone(tone) -> bool :
    sample = tone[0]
    for i in range(1,len(tone)):
        if tone[i] != sample:
            return False
    return True

if __name__ == "__main__":
    
    title = GetWebSourceTitle()
    urls = GetNewsUrl(title)


    for url in urls:
        articles = GetNewsArticleText(url)
        for article in articles:
            words = jieba.cut(article)
            for w in words:
                print(w)
                t = GetTone(w)
                print(CheckTone(t))
   
    '''
    s = "二敗要做線上測驗"
    s = re.split(r"[、，。（）：]",s)
    for word in s:
        words = jieba.cut(word)
        for w in words:
            print(w)
            t = GetTone(w)
            print(CheckTone(t))
    '''
