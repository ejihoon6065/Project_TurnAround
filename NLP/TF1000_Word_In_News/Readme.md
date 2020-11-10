## 한국경제뉴스제목 기사데이터에서 Unigram과 Bigram단어들의 TF를 count하고 Top1000단어들을 추출

### 뉴스데이터의 Feature 및 Labeling 방법 설명 : 
```python
-labeling : 해당 날짜의 다음날 코스피지수의 등락율에 따라 라벨링(등락율(per)이 양수면 1, 음수면 0)
-is_col : 기사제목상, 칼럼기사인 경우이면 1, 아니면 0
-label_rev : 코스피지수와 관계없는 기사들을 직접 2로 라벨링
```

### 뉴스데이터.xlsx : 한경뉴스의 1997.10.21 ~ 2020.06.15 기사제목 크롤링한 데이터 (크롤링내용은 News_Crawling_Preprocessing폴더 참고)

### Uni_Gram_By_Mecab_Top1000.xlsx : Uni-Gram에서 TF 내림차순으로 정렬하여 Top1000개의 단어들을 추출한 결과물

### Bi_Gram_By_Mecab_Top1000.xlsx : Bi-Gram에서 TF 내림차순으로 정렬하여 Top1000개의 단어들을 추출한 결과물

### Bigram_Words.xlsx : Bi-Gram에서 각 단어들의 BIgram단어들과 각각의 TF를 한개의 row로 나타낸 결과물
