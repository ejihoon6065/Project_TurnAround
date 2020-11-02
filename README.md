# 프로젝트명 : 자연어처리 기반의 주가분석 및 예측시스템
- 팀명 : Project_TurnAround
- 멘토 : 정좌연🗽 PE 
- 멘티 : 이지훈👤, 김서정✌, 구병진🎶, 강민재😁, 이문형😎


# 1. Model Structure
- 데이터 수집 모듈 : [app.py](https://github.com/quantylab/rltrader)_정형 데이터,   [app.py](https://github.com/quantylab/rltrader)_비정형 데이터
- 데이터 분석 모듈 : [app.py](https://github.com/quantylab/rltrader)_AutoML, Prophet, NLP,  [app.py](https://github.com/quantylab/rltrader)_Reinforcement Learning
- 실행 모듈 : [app.py](https://github.com/quantylab/rltrader)

# 2. Environment Setup
가상환경에서 설치하는 것을 권장함.

가상환경 설치방법 : conda create -n [원하는 가상환경이름]
- OS : Windows 10 x64
- IDE : PyCharm, Jupyter Notebook, Google Colaboratory
- Language : Python 3.7 (Anaconda 3.7)

# 3. Library Installation
## 1) Data Analysis
```bash
# (1) 행렬 연산
pip install numpy

# (2) 데이터 분석
pip install pandas

# (3) 시각화
pip install matplotlib
pip install seaborn
pip install mplfinance

# (4) 한국의 공휴일
pip install workalender

# (5) 날짜
pip install DateTime
```

## 2) Web Application
(1) streamlit 설치
```bash
pip install streamlit
```

## 3) Financial Data API
(1) Yahoo Finance API 설치
```bash
pip install yfinance --upgrade --no-cache-dir
```

(2) investing.com API 설치
```bash
pip install investpy
```

(3) KRX API 설치
```bash
pip install pykrx
```

(4) ta-lib 설치 - 기술적 분석 (보조지표)
```bash
pip install ta-lib
```
설치에 실패할 경우에는, [link](https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib)에서 버전에 맞는 파일을 다운로드해서 아래와 같이 설치함
- Ex) python 3.7/64비트 버전 사용시
```bash
pip install TA Lib‑0.4.19‑cp37‑cp37m‑win_amd64.whl
```

## 4) Prophet
(1) Prophet 설치
```bash
conda install -c conda-forge fbprophet
pip install pystan
pip install prophet
pip install fbprophet
```

## 5) AutoML
(1) pycaret 설치
```bash
pip install pycaret
```

## 6) Reinforcement Learning
(1) TensorFlow 1.15.2 설치
```bash
pip install tensorflow==1.15.2
```

(2) Keras 2.2.4 설치
```bash
pip install Keras=2.2.4
```

## 7) Natural Language Processing
<p>
<p align="Left">
    <a href="https://github.com/ejihoon6065/Project_TurnAround/blob/master/NLP/ReadMe.md">  
        <img alt="Contributor Covenant" src="https://img.shields.io/badge/NLP%20-Mecab%20-ff69b4.svg">
    </a>에서 자세한 설치 방법 확인
</p>

```bash
# (1) Konlpy 설치
pip install JPype1‑0.6.3‑cp37‑cp37m‑win_amd64.whl

# (2) Mecab 설치
pip install mecab_python-0.996_ko_0.9.2_msvc-cp37-cp37m-win_amd64.whl
```
# 4. Model Description
## 1) Data Collection Module : [DataCollectionModel.py](https://github.com/ejihoon6065/Project_TurnAround/blob/master/Main%20Code/webtest/DataCollectionModel.py)

## (1) Data Sources
- 정형 데이터 : [YahooFinance](https://finance.yahoo.com/), [investing.com](https://www.investing.com/), [krx](http://www.krx.co.kr/main/main.jsp)
- 비정형 데이터 : [한국경제신문](https://www.hankyung.com/)

## (2) Feature Description
All features of the data are described below : <p>
<p align="left">
    <a href="https://github.com/ejihoon6065/Project_TurnAround/blob/master/ReadMe_Data.md">  
        <img alt="Documentation" src="https://img.shields.io/website/http/huggingface.co/transformers/index.html.svg?down_color=red&down_message=offline&up_message=Data">
    </a>에서 모든 data features 확인
</p>

## 코스피 예측 모델
- 정형 데이터 : (1) 차트 데이터, (2) 투자지표, (3) 환율 데이터, (4) 원자재 데이터 (금값시세, 유가 등), (5) 금리 데이터, (6) 글로벌 주가지수
- 비정형 데이터 : (1) 뉴스 크롤링 데이터 --------추후 작성--------

## 와이지엔터테인먼트종목 주가 예측 모델
- 정형 데이터 : (1) 차트 데이터, (2) 와이지엔터테인먼트 투자지표, (3) 코스닥 주가지수 및 투자지표

## 전처리 데이터
- 정형 데이터 :  (1) 보조지표 (기술적 분석)
- 비정형 데이터 :  (1) 자연어 전처리 데이터 --------추후 작성--------

## 2) Data Analysis Module
--------추후 작성--------
Prophet, AutoML, Natural Language Processing, Reinforcement Learning

## 3) Run Module : [app.py](https://github.com/ejihoon6065/Project_TurnAround/blob/master/Main%20Code/webtest/app.py)
cmd 창을 열어서, webtest 디렉토리로 path를 설정하고, [app.py](https://github.com/ejihoon6065/Project_TurnAround/blob/master/Main%20Code/webtest/app.py)를 실행합니다.
```bash
# app.py 실행
streamlit run app.py
```
(1) 데이터를 자동으로 수집하기 때문에, 데이터를 수집하는 시간이 필요합니다.

(2) 데이터가 수집되고 난 후에, 예측하고 싶은 Date, Target, Method을 입력합니다.

<p align="left">
    <img src="https://github.com/ejihoon6065/Project_TurnAround/blob/master/image/tutorial_1.PNG" height="300px" width="600px">
</p>


(3) 분석 모델(또는 미리 학습된 모델)이 학습을 통해 분석 및 예측 결과를 도출합니다.

<p align="left">
    <img src="https://github.com/ejihoon6065/Project_TurnAround/blob/master/image/tutorial_2.PNG" height="400px" width="600px">
</p>

# 5. Development Notes
--------추후 작성--------

# Contributing
실용 중심 AI 개발자 양성 과정 씨에쓰리 산학프로젝트

# License & Reference
강화학습 모델 [QuantyLab](https://github.com/quantylab/rltrader)
