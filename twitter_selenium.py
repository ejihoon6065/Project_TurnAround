# -*- coding: utf-8 -*-
from selenium import webdriver 
from bs4 import BeautifulSoup 
import requests 
from selenium.webdriver.common.desired_capabilities import  DesiredCapabilities 
import time 
from selenium.webdriver.common.keys import Keys 
import datetime as dt 
import pandas as pd

"""
Created on Thu Feb 14 10:47:07 2019

@author: User
"""

browser = 'C:/Users/User/Desktop/python study/twitter_ws/chromedriver.exe'
RESULT_PATH ='C:/Users/User/Desktop/python study/twitter_ws/result/'  #결과 저장할 경로
driver = webdriver.Chrome(browser)

def crawler(query,startdate,enddate):
    startdate_lsit=startdate.split('-')
    start_d=startdate_lsit.pop()
    start_m=startdate_lsit.pop()
    start_y=startdate_lsit.pop()
    
    enddate_list=enddate.split('-')
    end_d=enddate_list.pop()
    end_m=enddate_list.pop()
    end_y=enddate_list.pop()
    
    
    startdate=dt.date(year=int(start_y),month=int(start_m),day=int(start_d)) #시작날짜 
    enddate=dt.date(year=int(end_y),month=int(end_m),day=int(end_d)+1) # 끝날짜
    untildate=dt.date(year=int(start_y),month=int(start_m),day=int(start_d)+1) # 시작날짜 +1 
    
    totaltweets=[] 
    totaldate=[]
    while not enddate==startdate: 
        
        url='https://twitter.com/search?q='+query+'%20since%3A'+str(startdate)+'%20until%3A'+str(untildate)+'&amp;amp;amp;amp;amp;amp;lang=eg' 
        driver.get(url) 
        html = driver.page_source 
        soup=BeautifulSoup(html,'html.parser') 
        
        lastHeight = driver.execute_script("return document.body.scrollHeight") 
        while True: 
            
            dailyfreq={'Date':startdate} 
    
            wordfreq=0 
            tweets=soup.find_all("p", {"class": "TweetTextSize"}) 
            date=soup.find_all("span",{"class": "_timestamp js-short-timestamp"})
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
            time.sleep(1) 
             
            newHeight = driver.execute_script("return document.body.scrollHeight") 
             
            if newHeight != lastHeight: 
                html = driver.page_source 
                soup=BeautifulSoup(html,'html.parser') 
                tweets=soup.find_all("p", {"class": "TweetTextSize"}) 
                date=soup.find_all("span",{"class": "_timestamp js-short-timestamp"})
                wordfreq=len(tweets) 
            else: 
                dailyfreq['Frequency']=wordfreq 
                wordfreq=0 
                startdate=untildate 
                untildate+=dt.timedelta(days=1) 
                dailyfreq={} 
                totaltweets.append(tweets) 
                totaldate.append(date)
                break 
    
            lastHeight = newHeight
            
    df = pd.DataFrame(columns=['date','message'])
    number=1 
    for i in range(len(totaltweets)): 
        for j in range(len(totaltweets[i])): 
            df = df.append({'date': (totaldate[i][j]).text,'message':(totaltweets[i][j]).text}, ignore_index=True) 
            number = number+1
    print(number)
    print(df)
    df.to_excel(RESULT_PATH+"twitter_result.xlsx",sheet_name='sheet1')


def main():
    info_main = input("="*50+"\n"+"트위터 크롤러"+"\n"+"입력 형식에 맞게 입력해주세요."+"\n"+" 시작하시려면 Enter를 눌러주세요."+"\n"+"="*50)
    query=input("검색어 입력(블록체인): ") 
    startdate=input("검색 시작 날짜 입력(2018-01-01): ") 
    enddate=input("검색 끝 날짜 입력(2018-01-02): ")
    
    crawler(query,startdate,enddate)
    
main()