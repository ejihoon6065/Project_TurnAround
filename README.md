# 프로젝트명 : 자연어처리 기반의 주가분석 및 예측시스템
- 팀명 : Project_TurnAround
- 멘토 : 정좌연🗽 PE 
- 멘티 : 이지훈👤, 김서정✌, 구병진🎶, 강민재😁, 이문형😎


# 1. Model Structure
- 데이터 수집 모듈 : [app.py](https://github.com/quantylab/rltrader)_정형 데이터,   [app.py](https://github.com/quantylab/rltrader)_비정형 데이터
- 데이터 분석 모듈 : [app.py](https://github.com/quantylab/rltrader)_AutoML, Prophet, NLP,  [app.py](https://github.com/quantylab/rltrader)_Reinforcement Learning
- 실행 모듈 : [app.py](https://github.com/quantylab/rltrader)

# 2. Environment Setup
가상환경에서 설치하는 것을 권장함( 가상환경 설치방법 : conda create -n [원하는 가상환경이름] )
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
[ReadMe.md](https://github.com/ejihoon6065/Project_TurnAround/blob/master/NLP/ReadMe.md)에서 자세한 설치 방법 확인
<p>
<p align="Left">
    <a href="https://github.com/ejihoon6065/Project_TurnAround/blob/master/NLP/ReadMe.md">  
        <img alt="Contributor Covenant" src="https://img.shields.io/badge/NLP%20-Mecab%20-ff69b4.svg">
    </a>
</p>

```bash
# (1) Konlpy 설치
pip install JPype1‑0.6.3‑cp37‑cp37m‑win_amd64.whl

# (2) Mecab 설치
pip install mecab_python-0.996_ko_0.9.2_msvc-cp37-cp37m-win_amd64.whl
```
# 4. Model Description
## 1) Data Collection Module

## Data Sources
- 정형 데이터 : [YahooFinance](https://finance.yahoo.com/), [investing.com](https://www.investing.com/), [krx](http://www.krx.co.kr/main/main.jsp)
- 비정형 데이터 : [한국경제신문](https://www.hankyung.com/)

## Feature Description
## 정형 데이터 (코스피 예측 모델)
## 1) 차트 데이터
| 지표명                        | 표현                    |
|-------------------------------|-------------------------|
| 년/월/일                      | Date                    |
| 시가                          | Open                    |
| 고가                          | High                    |
| 저가                          | Low                     |
| 종가                          | Close                   |
| 거래량                        | Volume                  |
| 코스피 기관 공매도 거래량     | kospi_inst_volume       |
| 코스피 개인 공매도 거래량     | kospi_indi_volume       |
| 코스피 외국인 공매도 거래량   | kospi_fore_volume       |
| 코스피 기타 공매도 거래량     | kospi_etc_volume        |
| 코스피 공매도 거래량 합계     | kospi_short_sell_volume |
| 코스피 기관 공매도 거래대금   | kospi_inst_value        |
| 코스피 개인 공매도 거래대금   | kospi_indi_value        |
| 코스피 외국인 공매도 거래대금 | kospi_fore_value        |
| 코스피 기타 공매도 거래대금   | kospi_etc_value         |
| 코스피 공매도 거래대금 합계   | kospi_short_sell_value  |

## 2) 투자지표


## 2) Data Analysis Module
Prophet, AutoML, Natural Language Processing, Reinforcement Learning
## 3) Run Module
app.py
# 5. Development Notes

# Contributing
실용 중심 AI 개발자 양성 과정 씨에쓰리 산학프로젝트

# License & Reference
강화학습 모델 [QuantyLab](https://github.com/quantylab/rltrader)
