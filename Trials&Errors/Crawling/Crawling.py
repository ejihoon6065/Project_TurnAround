#!/usr/bin/env python
# coding: utf-8

from wordcloud import WordCloud, STOPWORDS
import urllib.request
from urllib.request import urlopen
import requests 
from urllib.request import HTTPError
from bs4 import BeautifulSoup
import pandas as pd

df = pd.read_excel('./data/kospi.xls', sheet_name = 'Sheet4')

df['minus2'].astype(str)

list_date = df['minus2'].dropna().astype(str).values.tolist()

list1 = []

for i in range(len(list_date)):
    year = str(list_date[i])[0:4]
    month = str(list_date[i])[5:7]
    day = str(list_date[i])[8:10]
    print(year,month,day)

    list2 = []
    list2.append(str(year)+'.'+month+'.'+day)
    for j in range(15) : # range : 페이지 수 입력
        page = j+1
        url = f'https://hankyung.com/economy?date={year}.{month}.{day}&page={page}'
        #url = 'https://www.hankyung.com/economy?date=2020.04.01'
        response = requests.get(url)
        html = response.text
        #print(html)
        soup = BeautifulSoup(response.content.decode('UTF-8','replace'))
        #print(soup)
        #tit1 = soup.find_all('div', 'article') # 1~ 10
        tit2 = soup.find_all('h3', 'tit') # 나머지 
        #print(tit1)
        #print(tit2)

        for i in range(len(tit2)):
            a=str(tit2[i])
            a2 = a.split('>')[2]
            a3 = a2.split('<')[0]
            list2.append(a3)
    list1.append(list2)

pd_list = pd.DataFrame(list1)
pd_list.to_csv("result.csv", mode='w', encoding='utf-8-sig', index=False)
# error뜰 때 인코딩을 utf-8-sig로 수정


