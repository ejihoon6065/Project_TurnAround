#!/usr/bin/env python
# coding: utf-8

# # 1. 라이브러리

import DataCollectionModel
import app

import pandas as pd #데이터 분석
import numpy as np #행렬 연산

import datetime as dt # 날짜타입 사용
import random # 시드 제어
import copy # 복사 기능

import seaborn as sns # 시각화
import matplotlib.pyplot as plt # 시각화

from workalendar.asia import SouthKorea # 한국의 공휴일
import random # 시드 제어

import talib as ta # 기술적 분석 (보조지표)

from pycaret.regression import * # AutoML pycaret
from pycaret.classification import * # AutoML pycaret
from fbprophet import Prophet # Prophet
from fbprophet.diagnostics import cross_validation # Prophet
from fbprophet.diagnostics import performance_metrics # Prophet
from fbprophet.plot import plot_cross_validation_metric # Prophet

import yfinance as yf # yahoo finance API
import investpy # investing.com API
from pykrx import stock # krx API
from pykrx.website.krx.bond.wrap import KrxBond # krx bond API

class Prophet_:

    def __init__(self, date):
        self.date = dt.datetime.strptime(date, '%Y%m%d').date().strftime("%Y-%m-%d")
        self.pred_days=1

    def prophet_kospi(self, model_kospi):
        # # 1) 코스피
        self.model_kospi = model_kospi
        self.df = copy.deepcopy(self.model_kospi)
        self.df['date'] = pd.to_datetime(self.df.index)
        self.data = self.df[['date', 'Close']].reset_index(drop=True)
        self.data = self.data.rename(columns={'date': 'ds', 'Close': 'y'})

        # 데이터의 추이 파악
        # self.data.plot(x='ds', y='y', figsize=(16, 8))

        # 하이퍼 파라미터
        #self.prop_model = Prophet(
        #     growth='linear',
        #     #changepoints=cp_1,
        #     #n_changepoints=25,
        #     changepoint_range=0.95,
        #     yearly_seasonality='auto',
        #     weekly_seasonality='auto',
        #     daily_seasonality='auto',
        #     holidays=None,
        #     seasonality_mode='additive',
        #     seasonality_prior_scale=10.0,
        #     holidays_prior_scale=10.0,
        #     changepoint_prior_scale=0.05,
        #     mcmc_samples=0,
        #     interval_width=0.8,
        #     uncertainty_samples=1000,
        #     stan_backend=None,
        # )

        self.prop_model = Prophet(yearly_seasonality='auto',
                             weekly_seasonality='auto',
                             daily_seasonality='auto',
                             changepoint_prior_scale=0.15,
                             changepoint_range=0.9
                             )
        print("h")
        self.model = self.prop_model
        self.model.add_country_holidays(country_name='KR')
        self.model.fit(self.data)

        self.kor_holidays = pd.concat([pd.Series(np.array(SouthKorea().holidays(2020))[:, 0]),
                                  pd.Series(np.array(SouthKorea().holidays(2021))[:, 0])]).reset_index(drop=True)

        self.future = self.model.make_future_dataframe(periods=self.pred_days)
        self.future = self.future[self.future.ds.dt.weekday != 5]
        self.future = self.future[self.future.ds.dt.weekday != 6]
        for self.kor_holiday in self.kor_holidays:
            self.future = self.future[self.future.ds != self.kor_holiday]

        self.forecast = self.model.predict(self.future)
        self.forecast[['ds', 'yhat', 'yhat_upper', 'yhat_lower']]

        # model.plot(forecast)
        # fig2 = model.plot_components(forecast)

        # figure = model.plot(forecast)
        # for changepoint in model.changepoints:
        #    plt.axvline(changepoint,ls='--', lw=1)
        # figure.legend(loc=2)

        # df.shape

        # # Cross Validation
        #
        # - For measuring forecast error by comparing the predicted values with the actual values
        # - initial:the size of the initial training period
        # - period : the spacing between cutoff dates
        # - horizon : the forecast horizon((ds minus cutoff)
        # - By default, the initial training period is set to three times the horizon, and cutoffs are made every half a horizon

        #self.cv = cross_validation(self.model, initial='534 days', period='20 days', horizon='134 days')
        #self.df_pm = performance_metrics(self.cv)

        # # Visualizing Performance Metrics
        # - cutoff: how far into the future the prediction was
        #plot_cross_validation_metric(self.cv, metric='rmse')

        # 실제값
        self.actual_value = float(self.data[self.data['ds'] == self.data.iloc[-1].ds]['y'])
        print(self.actual_value)
        # 예측값
        self.predict_value = float(self.forecast[self.forecast['ds'] == self.date]['yhat'])
        print(self.predict_value)

        if self.actual_value < self.predict_value:
            print("actual_value : ", self.actual_value, ", predict_value : ", self.predict_value, ", 주가 상승 예상 -> 매수")
            return '1'
        else:
            print("actual_value : ", self.actual_value, ", predict_value : ", self.predict_value, ", 주가 하락 예상 -> 매도")
            return '0'






"""
# # 2) YG

# In[42]:


model_yg.describe()


# In[43]:


df=copy.deepcopy(model_yg)


# In[44]:


#df.date = df.date.astype(str)
#df.date = df.date.str[:4] + '-' + df.date.str[4:6] + '-' + df.date.str[6:]
df['date'] = pd.to_datetime(df.index)

data = df[['date', 'Close']].reset_index(drop=True)

data = data.rename(columns={'date': 'ds', 'Close': 'y'})

data.head()


# In[45]:


# 데이터의 추이 파악
data.plot(x='ds', y='y', figsize=(16, 8))


# In[75]:


# cp=['2019-10-23', '2019-11-04', '2019-11-13', '2019-11-22', '2019-12-04', '2019-12-13', '2019-12-26', '2020-01-08', '2020-01-17', '2020-01-31', '2020-02-11', '2020-02-20', '2020-03-03', '2020-03-12', '2020-03-23', '2020-04-02', '2020-04-13', '2020-04-23', '2020-05-08', '2020-05-19', '2020-05-29', '2020-06-09', '2020-06-18', '2020-06-30', '2020-07-09']

cp_spc=['2020-08-11',
 '2020-08-12',
 '2020-08-13',
 '2020-08-18',
 '2020-08-19',
 '2020-08-20',
 '2020-08-26',
 '2020-08-28',
 '2020-08-31',
 '2020-09-02',
 '2020-09-03',
 '2020-09-07',
 '2020-09-08']

cp_default=['2018-10-29',
    '2018-11-19',
    '2018-12-11',
    '2019-01-04',
    '2019-01-29',
    '2019-02-22',
   '2019-03-19',
   '2019-04-10',
   '2019-05-03',
   '2019-05-27',
   '2019-06-19',
   '2019-07-10',
   '2019-08-01',
   '2019-08-26',
   '2019-09-20',
   '2019-10-15',
   '2019-11-07',
   '2019-11-29',
   '2019-12-26',
   '2020-01-20',
   '2020-02-13',
   '2020-03-05',
   '2020-03-30',
   '2020-04-21',
   '2020-05-18']
cp=cp_default+cp_spc
cp


# In[76]:


from fbprophet import Prophet
from workalendar.asia import SouthKorea


#     growth='linear',
#     #changepoints=cp_1,
#     #n_changepoints=25,
#     changepoint_range=0.95,
#     yearly_seasonality='auto',
#     weekly_seasonality='auto',
#     daily_seasonality='auto',
#     holidays=None,
#     seasonality_mode='additive',
#     seasonality_prior_scale=10.0,
#     holidays_prior_scale=10.0,
#     changepoint_prior_scale=0.05,
#     mcmc_samples=0,
#     interval_width=0.8,
#     uncertainty_samples=1000,
#     stan_backend=None,

m = Prophet(yearly_seasonality='auto',
     weekly_seasonality='auto',
     daily_seasonality='auto',
     changepoints=cp
     changepoint_range=0.8,
     changepoint_prior_scale=0.1
     )
m.fit(data)
pred_days=int(input('How many days do you want to predict?'))
kor_holidays = pd.concat([pd.Series(np.array(SouthKorea().holidays(2019))[:, 0]), pd.Series(np.array(SouthKorea().holidays(2020))[:, 0])]).reset_index(drop=True)
future = m.make_future_dataframe(periods=pred_days)

future = future[future.ds.dt.weekday != 5]
future = future[future.ds.dt.weekday != 6]
for kor_holiday in kor_holidays:
    future = future[future.ds != kor_holiday]
    
future.tail()
forecast = m.predict(future)


# In[77]:


forecast[ [ 'ds', 'yhat', 'yhat_lower', 'yhat_upper' ] ].tail(pred_days)


# In[78]:


m.plot(forecast)


# In[79]:


m.plot_components( forecast)


# In[80]:


figure = m.plot(forecast)
for changepoint in m.changepoints:
    plt.axvline(changepoint,ls='--', lw=1)
figure.legend(loc=2)


# In[81]:


print(m.changepoints)


# In[72]:


# 예측한 값만 표로 보기
pred=forecast.tail(pred_days)
pred


# In[ ]:


# plt.rc('font', family='NanumBarunGothic') 

# fig = plt.figure(figsize=(15,12))
# ax1 = fig.add_subplot(211)
# ax1.plot(y['종가'],label='Y')
# ax1.plot(pred['yhat'],color='red',label='Yhat')
# ax1.plot(pred['yhat_lower'],color='green',label='Yhat_Lower')
# ax1.plot(pred['yhat_upper'],color='green',label='Yhat_Upper')
# ax1.set_xlabel('Date')
# ax1.set_ylabel('Y')
# ax1.legend(loc='best')
# plt.show


# 

"""
