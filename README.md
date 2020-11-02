# 자연어처리 기반의 주가분석 및 예측시스템
- 팀명 : Project_TurnAround
- 멘토 : 정좌연🗽 PE 
- 멘티 : 이지훈👤, 김서정✌, 구병진🎶, 강민재😁, 이문형😎

# 환경설정
가상환경에서 설치하는 것을 권장함
* 가상환경 설치방법 : conda create -n [원하는 가상환경이름]
- OS : Windows 10 x64
- IDE : PyCharm, Jupyter Notebook, Google Colaboratory
- Language : Python 3.7 (Anaconda 3.7)

# 라이브러리
## 1. Data Analysis
행렬 연산
```bash
pip install numpy
```

데이터 분석
```bash
pip install pandas
```

시각화
```bash
pip install matplotlib
pip install seaborn
pip install mplfinance
```

한국의 공휴일
```bash
pip install workalender
```

날짜
```bash
pip install DateTime
```

## 2. Web Application
streamlit 설치
```bash
pip install streamlit
```

## 3. Financial data API
Yahoo Finance API 설치
```bash
pip install yfinance --upgrade --no-cache-dir
```

investing.com API 설치
```bash
pip install investpy
```

KRX API 설치
```bash
pip install pykrx
```

기술적 분석 (보조지표) : ta-lib 설치
```bash
pip install ta-lib
```
설치에 실패할 경우에는, [link](https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib)에서 버전에 맞는 파일을 다운로드해서 아래와 같이 설치함
- Ex) python 3.7/64비트 버전 사용시
```bash
pip install TA Lib‑0.4.19‑cp37‑cp37m‑win_amd64.whl
```

## 4. Prophet
Prophet 설치
```bash
conda install -c conda-forge fbprophet
pip install pystan
pip install prophet
pip install fbprophet
```

## 5. AutoML
pycaret 설치
```bash
pip install pycaret
```

## 6. Reinforcement Learning
- Anaconda 3.7+
TensorFlow 1.15.2 설치
```bash
pip install tensorflow==1.15.2
```


Keras 2.2.4 설치
```bash
pip install Keras=2.2.4
```

## 7. Natural Language Processing
[NLP.md](https://github.com/ejihoon6065/Project_TurnAround/blob/master/NLP/ReadMe.md)에서 설치 방법 확인

```python
import foobar

foobar.pluralize('word') # returns 'words'
foobar.pluralize('goose') # returns 'geese'
foobar.singularize('phenomena') # returns 'phenomenon'
```

# Contributing
실용 중심 AI 개발자 양성 과정 씨에쓰리 산학프로젝트

# License & Reference
강화학습 모델 [QuantyLab](https://github.com/quantylab/rltrader)
