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
import json

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
r = requests.get(url)
web_content = r.text
soup = BeautifulSoup(web_content,'lxml')
title = soup.find_all('h3',class_= class_name)

refs = [t.find('a')['href'].replace(".","https://news.google.com") for t in title]

print("--------------------------------------")
urls = [requests.get(t).url for t in refs]
print(urls)


print("--------------------------------------")
titles = [t.find('a').text for t in title]
print(titles)
print("--------------------------------------")

r = requests.get(urls[0])
content = r.text
soup = BeautifulSoup(content,'lxml')
articles = soup.find_all("p")
for article in articles:
    print(article.text)
'''
for t in titles:
    print(t)
    ans = pinyin(t,style = Style.TONE3)
    for s in ans:
        print(s[0][-1])
'''
