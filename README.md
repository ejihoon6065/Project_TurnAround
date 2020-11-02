# 프로젝트명 : 자연어처리 기반의 주가분석 및 예측시스템
- 팀명 : Project_TurnAround
- 멘토 : 정좌연🗽 PE 
- 멘티 : 이지훈👤, 김서정✌, 구병진🎶, 강민재😁, 이문형😎


# 1. Model Structure
- 데이터 수집 모듈 : [app.py](https://github.com/quantylab/rltrader)_정형 데이터,   [app.py](https://github.com/quantylab/rltrader)_비정형 데이터
- 데이터 분석 모듈 : [app.py](https://github.com/quantylab/rltrader)_AutoML, Prophet, NLP,  [app.py](https://github.com/quantylab/rltrader)_Reinforcement Learning
- 실행 모듈 : [app.py](https://github.com/quantylab/rltrader)

# 2. Environment Setup
가상환경에서 설치하는 것을 권장함. 가상환경 설치방법 : conda create -n [원하는 가상환경이름]
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
| 구분     | 지수명(지표명)                      | 표현                     |
|----------|-------------------------------------|--------------------------|
| 대표지수 | 코스피 200 종가                     | kospi_200_Close          |
|          | 코스피 200 중소형주 종가            | kospi_200_midsmall_Close |
|          | 코스피 200 초대형제외 종가          | kospi_200_exbig_Close    |
| 섹터지수 | 코스피 200 커뮤니케이션 서비스 종가 | kospi_200_comm_Close     |
|          | 코스피 200 건설 종가                | kospi_200_const_Close    |
|          | 코스피 200 중공업 종가              | kospi_200_heavy_Close    |
|          | 코스피 200 철강/소재 종가           | kospi_200_steel_Close    |
|          | 코스피 200 에너지/화학 종가         | kospi_200_energy_Close   |
|          | 코스피 200 정보기술 종가            | kospi_200_info_Close     |
|          | 코스피 200 금융 종가                | kospi_200_finance_Close  |
|          | 코스피 200 생활소비재 종가          | kospi_200_life_Close     |
|          | 코스피 200 경기소비재 종가          | kospi_200_economy_Close  |
|          | 코스피 200 산업재 종가              | kospi_200_industy_Close  |
|          | 코스피 200 헬스케어 종가            | kospi_200_health_Close   |

## 3) 환율 데이터
| 지표명            | 표현                    |
|-------------------|-------------------------|
| 달러/원 환율 종가 | exchange_rate_usd_Close |
| 유로/원 환율 종가 | exchange_rate_eur_Close |
| 엔/원 환율 종가   | exchange_rate_jpy_Close |
| 위안/원 환율 종가 | exchage_rate_cny_Close  |

## 4) 원자재 데이터 (금값시세, 유가 등)
| 지표명                   | 표현                    |
|--------------------------|-------------------------|
| comex 금 시세 종가       | comex_gold_Close        |
| comex 미니 금 시세 종가  | comex_mini_gold_Close   |
| comex 은 시세 종가       | comex_silver_Close      |
| comex 미니 은 시세 종가  | comex_mini_silver_Close |
| comex 동(구리) 시세 종가 | comex_copper_Close      |
| 미국 플래티넘 시세 종가  | platinum_Close          |
| 미국 팔라듐 시세 종가    | palladium_Close         |
| WTI유 시세 종가          | crude_oil_Close         |
| 가솔린 RBOB 시세 종가    | rbob_gasoline_Close     |
| 미국 천연가스 시세 종가  | natural_gas_Close       |
| 미국 난방유 시세 종가    | heating_oil_Close       |

## 5) 금리 데이터
| 지표명                            | 표현               |
|-----------------------------------|--------------------|
| 미국 국채 수익률 (13주) 종가      | treasury_13w_Close |
| 미국 국채 수익률 (5년) 종가       | treasury_5y_Close  |
| 미국 국채 수익률 (10년) 종가      | treasury_10y_Close |
| 미국 국채 수익률 (30년) 종가      | treasury_30y_Close |
| 한국 채권수익률 (지표수익률) 3년  | treasury_krx_3y    |
| 한국 채권수익률 (지표수익률) 5년  | treasury_krx_5y    |
| 한국 채권수익률 (지표수익률) 10년 | treasury_krx_10y   |
| 한국 채권수익률 (지표수익률) 20년 | treasury_krx_20y   |
| 한국 채권수익률 (지표수익률) 30년 | treasury_krx_30y   |

## 6) 글로벌 주가지수
| 지수명(지표명)        | 표현               |
|-----------------------|--------------------|
| Vix 종가              | vix_Close          |
| KOSPI Volatility 종가 | vkospi_Close       |
| Bitcoin USD 종가      | bitcoin_Close      |
| S&P 500 종가          | snp_500_Close      |
| Dow Jones 종가        | dow_jones_Close    |
| NASDAQ 종가           | nasdaq_Close       |
| NYSE 종가             | nyse_Close         |
| AMEX 종가             | amex_Close         |
| Russell 2000 종가     | russell_2000_Close |
| DAX 종가              | dax_Close          |
| Nikkei 225 종가       | nikkei_225_Close   |
| HANG SENG 종가        | hang_seng_Close    |
| SSE 종가              | sse_Close          |
| ESTX 50 종가          | estx_50_Close      |
| EURONEXT 100 종가     | euronext_100_Close |


## 정형 데이터 (와이지엔터테인먼트종목 주가 예측 모델)
## 1) 차트 데이터
| 지표명     | 표현         |
|------------|--------------|
| 시가       | Open         |
| 고가       | High         |
| 저가       | Low          |
| 종가       | Close        |
| 거래량     | Volume       |
| 시가총액   | Market_Value |
| 거래대금   | Value        |
| 상장주식수 | Num_Stock    |

## 2) 와이지엔터테인먼트 투자지표
| 지표명                | 표현                 |
|-----------------------|----------------------|
| 와이지 공매도         | yg_short_sell        |
| 와이지 잔고           | yg_balance           |
| 와이지 공매도금액     | yg_short_sell_value  |
| 와이지 잔고금액       | yg_balance_value     |
| 와이지 공매도거래량   | yg_short_sell_volume |
| 와이지 총거래량       | yg_total_volume      |
| 와이지 공매도 비중    | yg_short_sell_rate   |
| 와이지 공매도거래대금 | yg_short_sell_value  |

## 3) 코스닥 주가지수 및 투자지표
| 구분                 | 지수명(지표명)                 | 표현                     |
|----------------------|--------------------------------|--------------------------|
| 종합지수             | 코스닥 시가                    | kosdaq_Open              |
|                      | 코스닥 고가                    | kosdaq_High              |
|                      | 코스닥 저가                    | kosdaq_Low               |
|                      | 코스닥 종가                    | kosdaq_Close             |
|                      | 코스닥 거래량                  | kosdaq_Volume            |
|                      | 코스닥 기관 공매도 거래량      | kosdaq_inst_volume       |
|                      | 코스닥 개인 공매도 거래량      | kosdaq_indi_volume       |
|                      | 코스닥 외국인 공매도 거래량    | kosdaq_fore_volume       |
|                      | 코스닥 기타 공매도 거래량      | kosdaq_etc_volume        |
|                      | 코스닥 공매도 거래량 합계      | kosdaq_short_sell_volume |
|                      | 코스닥 기관 공매도 거래대금    | kosdaq_inst_value        |
|                      | 코스닥 개인 공매도 거래대금    | kosdaq_indi_value        |
|                      | 코스닥 외국인 공매도 거래대금  | kosdaq_fore_value        |
|                      | 코스닥 기타 공매도 거래대금    | kosdaq_etc_value         |
|                      | 코스닥 공매도 거래대금 합계    | kosdaq_short_sell_value  |
| 대표지수             | 코스닥 150 종가                | kosdaq_150_Close         |
| 섹터지수             | 코스닥 150 커뮤니케이션 서비스 | kosdaq_150_comm_Close    |
| 산업별 지수          | 코스닥 오락, 문화              | kosdaq_enter_Close       |
| 시가총액 규모별 지수 | 코스닥 대형주                  | kosdaq_large_Close       |
| 소속부 지수          | 코스닥 우량기업부              | kosdaq_super_Close       |


## 정형 데이터 (전처리 데이터)
## 1) 보조지표 (기술적 분석)
| 지표명                                   | 파라미터 값            | 표현                                               |
|------------------------------------------|------------------------|----------------------------------------------------|
| 이평선 (이동평균, 지수평균, 가중평균)    | 5, 10, 20, 30, 60, 120 | 종가, 거래량에 적용<br>ma_xxx, ema_xxx, wma_xxx    |
| 볼린저밴드                               | 20, 2                  | ubb, mbb, lbb                                      |
| MACD (이동평균수렴확산)                  | 12, 26                 | macd, macdsignal9, macdhist                        |
| RSI (상대강도지수)                       | 14                     | rsi                                                |
| 스토캐스틱                               | 5, 3<br>14, 5          | slowk, slowd, fastk, fastd<br>fastk_rsi, fastd_rsi |
| CCI (Commodity Channel Index)            | 14                     | cci                                                |
| Williams’%R                              | 14                     | willR                                              |
| parabolic SAR                            |                        | sar                                                |
| ADX (Average Directional Movement Index) | 14                     | adx                                                |
| plusDI (Plus Directional Indicator)      | 14                     | plus_di                                            |
| plusDM (Plus Directional Movement)       | 14                     | plus_dm                                            |
| ATR (Average True Range)                 | 14                     | atr                                                |
| OBV (On Balance Volume)                  |                        | obv                                                |
| Variance                                 | 5, 1                   | var                                                |
| Three Line Strike                        |                        | line_str                                           |
| Three Black Crows                        |                        | blk_crw                                            |
| Evening Star                             |                        | evn_star                                           |
| Abandoned Baby                           |                        | abn_baby                                           |

## 2) Data Analysis Module
Prophet, AutoML, Natural Language Processing, Reinforcement Learning
## 3) Run Module
app.py
# 5. Development Notes

# Contributing
실용 중심 AI 개발자 양성 과정 씨에쓰리 산학프로젝트

# License & Reference
강화학습 모델 [QuantyLab](https://github.com/quantylab/rltrader)
