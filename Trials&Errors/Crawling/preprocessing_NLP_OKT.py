#!/usr/bin/env python
# coding: utf-8

# # AutoML을 위한 데이터 전처리 정리
# #### 뉴스를 크롤링한 형식이 date, 요일, labeling이 빠져있는 형태임... 크롤링file  + 전처리file 할때  date, 요일, labeling 을 추가 해주어야 들어가는 데이터가 맞음.

import pandas as pd
from tqdm import tqdm
import re
from konlpy.tag import Okt
# from konlpy.tag import Mecab
# tokenizer는 okt, mecab 중 선택하여 사용 .

# 사용할 데이터 경로, 결과 데이터 경로, tokenizer와 stopwords 를 정의하고 사용하면 됩니다.

path = './뉴스데이터통합테스트.xlsx' # path는 원데이터 경로 / 데이터는 labeling, 요일, date 가 있는 크롤링 뉴스 데이터
result_path = './automl_data.csv' # 결과 데이터가 저장될 path

tokenizer = Okt()
#tokenizer = Mecab()
stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']

# 데이터를 정의하고 원데이터를 한열로 펴주는 역할. 
data = pd.read_excel(path)

titles = [] 
for i in range(len(data.loc[0])-3): # data.loc[0] data의 0행을 반환, 앞의 3개열을 제외하고 4번째 열부터 시작 하기위해 -3 를 해준다.
    titles.append(data.iloc[0,i+3]) # 1,2,3 열을 제외하고 4번째 열부터 시작. 데이터에 date, labeling 만 있다면 숫자는 2로 바꾼다.

data_temp = pd.DataFrame(titles, columns=['title']) # concat을 위해 첫번째 행을 가지고 data frame 1개를 만든다.
data_temp = data_temp.dropna()
data_temp['date'] = data.loc[0]['date']
data_temp['labeling'] = data.loc[0]['labeling']


for j in range(len(data)-1) : # 첫번째 행을 제외한 나머지 행을 돌며 뉴스를 일렬로 
    titles = [] 
    for i in range(len(data.loc[j+1])-3): # 2번째 행, 4번째 열 부터 for 문을 돈다. 왜냐하면 첫번째 행은 data_temp로 만들었고, 1,2,3 열 에는 title 값이 들어가 있지 않기 때문이다.
        titles.append(data.iloc[j+1,i+3])

    data_temp2 = pd.DataFrame(titles, columns=['title']) 
    data_temp2 = data_temp2.dropna()
    data_temp2['date'] = data.loc[j+1]['date']
    data_temp2['labeling'] = data.loc[j+1]['labeling']
    
    
    data_temp = pd.concat([data_temp, data_temp2]) # 첫번째 행의 일렬 데이터와, 두번째행 부터 끝행 까지의 일렬 데이터를 합쳐준다. 


#print('중복 제거전 :' ,len(data_temp['labeling'])) #확인용 코드 
#print('라벨이 0, 1인 뉴스 개수 :',len(data_temp[data_temp['labeling'] == 0]) + len(data_temp[data_temp['labeling'] == 1])) #확인용 코드 
label_zero = data_temp[data_temp['labeling'] == 0] # 라벨이 0인것만 가지고 온다. 
label_one = data_temp[data_temp['labeling'] == 1] # 라벨이 1인것만 가지고온다. 
data = pd.concat([label_zero, label_one])
#print('중복 제거후 :',len(data)) #결과 확인용 코드 

clean_title = []
for text in data['title']:
  temp = re.sub('[-=+,#/\?:^$.@*\"※~>`\'…》]', '', text) # 특수문자를 제거하여 clean title을 만들어준다.
  clean_title.append(temp)
data['clean_title'] = clean_title

clean_title = data['clean_title'].tolist() # clean title을 이용하여 words top 1000을 만들어 주기위해 리스트에 title을 넣어준다.
title_words_list = [] # 각 title을 쪼갠 words값들이 들어가는 list 를 만들어준다. [[title1 words], [title2 words], ....]

for i in tqdm(range(len(clean_title))):
  temp_X = []
  temp_X = tokenizer.morphs(clean_title[i], stem=True) # 토큰화
  temp_X = [word for word in temp_X if not word in stopwords] # 불용어 제거
  temp_X = [word for word in temp_X if len(word) > 1]
  title_words_list.append(temp_X)
data['word'] = title_words_list



words_list = [y for x in title_words_list for y in x] # 2차원 list 를 1차원 list 로 만들어준다. 
words_cnt = []

i = 0
for words in tqdm(set(words_list)):
    words_cnt.append((words,words_list.count(words))) # 중복을 제거한 words_list안에서 words값을 count 한다. 
#    i += 1  #디버깅용
#    if i ==100 :break
#print(words_cnt)

words_cnt.sort(key = lambda x:x[1], reverse = True) #튜플의 1인덱스(count) 기반으로 sort함
words_top1000 = words_cnt[:1000] # count한 word의 1000위 까지를 가져온다. 
words_top = []
for word in tqdm(words_top1000):
    words_top.append(word[0])

date_label = data[['date', 'labeling']].drop_duplicates('date') # data의 date를 기준으로 가장 첫번째 값을 남기고 중복 데이터는 모두 제거한다.  
automl_data = pd.DataFrame(columns = words_top) # words_top 1000으로 column을 지정.
automl_data['date'] = date_label['date']
automl_data['labeling'] = date_label['labeling']
automl_data.sort_values(by=['date'], inplace =True)
automl_data.reset_index(inplace=True) # index를 리셋 
del automl_data['index'] # 옛날인덱스를 제거

automl_data_columns = [automl_data_column for automl_data_column in automl_data.columns] 
automl_data_columns.pop() # labeling 을 빼줌.
automl_data_columns.pop() # date 를 빼줌.
automl_data_columns

date_list = automl_data['date'].tolist()

for i in tqdm(range(len(date_list))):

    news = data[data['date'] == date_list[i]]['word'].tolist() # automl data의 date에 맞는 data의 word만 가져와 list형태로 
    X_train = [m for j in news for m in j] # [['title1_word1','title1_word2',... ], ['title2_word1','title2_word2'... ]...] 의 형태를 ['word1', 'word2'...] 로 바꾸어준다.

    for automl_data_column in automl_data_columns:
        automl_data.loc[[i],[automl_data_column]] = X_train.count(automl_data_column) # automl_data 빈칸에

automl_data.to_csv(result_path, encoding='utf-8-sig')


