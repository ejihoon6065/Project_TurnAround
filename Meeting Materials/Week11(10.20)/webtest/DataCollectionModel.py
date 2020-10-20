#!/usr/bin/env python
# coding: utf-8

# # 1. 라이브러리

import pandas as pd #데이터 분석
import numpy as np #행렬 연산

import datetime as dt # 날짜타입 사용
import random # 시드 제어

import seaborn as sns # 시각화
import matplotlib.pyplot as plt # 시각화

from workalendar.asia import SouthKorea # 한국의 공휴일
import random # 시드 제어

import talib as ta # 기술적 분석 (보조지표)

from pycaret.regression import * # AutoML pycaret
from pycaret.classification import * # AutoML pycaret
from fbprophet import Prophet # Prophet

import yfinance as yf # yahoo finance API
import investpy # investing.com API
from pykrx import stock # krx API
from pykrx.website.krx.bond.wrap import KrxBond # krx bond API


# # 2. 입력 데이터

# 1) 데이터 수집기간 입력

class DataCollection:
    
    def __init__(self, date):
        self.date = date

        # 데이터 수집기간 입력
        self.st_date = dt.date(2020,4,1)
        self.ed_date = dt.datetime.strptime(self.date, '%Y%m%d').date()

        # yahoo finance 양식, ex) yyyy-mm-dd
        self.start_date = self.st_date.strftime("%Y-%m-%d")
        self.end_date = (self.ed_date + dt.timedelta(days=1)).strftime("%Y-%m-%d")

        # investing.com 양식, ex) dd/mm/yyyy
        self.start_date_ = dt.datetime.strptime(self.st_date.strftime("%Y%m%d"), "%Y%m%d").strftime('%d/%m/%Y')
        self.end_date_ = dt.datetime.strptime(self.ed_date.strftime("%Y%m%d"), "%Y%m%d").strftime('%d/%m/%Y')

        # krx 양식 ex) yyyymmdd
        self.start_date__ = dt.datetime.strftime(self.st_date, "%Y%m%d")
        self.end_date__ = dt.datetime.strftime(self.ed_date, "%Y%m%d")


    # 피쳐 스케일링
    def feature_scaling(df, scaling_strategy="min-max", column=None):
        if column == None:
            column = [column_name for column_name in df.columns]
        for column_name in column:
            if scaling_strategy == "min-max":
                df[column_name] = (df[column_name] - df[column_name].min()) / (
                        df[column_name].max() - df[column_name].min())
            elif scaling_strategy == "z-score":
                df[column_name] = (df[column_name] - df[column_name].mean()) / (df[column_name].std())
        return df


    # # 2. 데이터 수집 (코스피지수 예측 모델)
    def kospi_collection(self):
        # 1) 코스피 차트 데이터 및 투자지표

        # 종합지수 (코스피) 차트 데이터
        self.kospi_ = stock.get_index_ohlcv_by_date(self.start_date__, self.end_date__, "1001")
        self.kospi_.columns = ['Open','High','Low','Close','Volume']

        # 코스피 투자자별 공매도 거래량
        self.kospi_short_sell_volume = stock.get_shorting_investor_volume_by_date(self.start_date__, self.end_date__, "KOSPI")
        self.kospi_short_sell_volume.columns = ['kospi_inst_volume','kospi_indi_volume','kospi_fore_volume','kospi_etc_volume','kospi_short_sell_volume']
        # 코스피 투자자별 공매도 거래대금
        self.kospi_short_sell_value = stock.get_shorting_investor_price_by_date(self.start_date__, self.end_date__, "KOSPI")
        self.kospi_short_sell_value.columns = ['kospi_inst_value','kospi_indi_value','kospi_fore_value','kospi_etc_value','kospi_short_sell_value']

        # 참고
        # 코스피 항목별 시장 거래량
        #kospi_market_volume = stock.get_market_trading_volume_by_date(self.start_date__, self.end_date__, "KOSPI")
        # 코스피 항목별 시장 거래대금
        #kospi_market_value = stock.get_market_trading_value_by_date(self.start_date__, self.end_date__, "KOSPI")


        # 2) 코스피 관련 주가지수

        # 대표지수 (코스피 200)
        self.kospi_200_ = stock.get_index_ohlcv_by_date(self.start_date__, self.end_date__, "1028")
        self.kospi_200_.columns = ['kospi_200_Open','kospi_200_High','kospi_200_Low','kospi_200_Close','kospi_200_Volume']
        self.kospi_200_ = self.kospi_200_.drop(['kospi_200_Open','kospi_200_High','kospi_200_Low','kospi_200_Volume'], axis=1)
        # 대표지수 (코스피 200 중소형주)
        self.kospi_200_midnsmall_ = stock.get_index_ohlcv_by_date(self.start_date__, self.end_date__, "1167")
        self.kospi_200_midnsmall_.columns = ['kospi_200_midnsmall_Open','kospi_200_midnsmall_High','kospi_200_midnsmall_Low','kospi_200_midnsmall_Close','kospi_200_midnsmall_Volume']
        self.kospi_200_midnsmall_ = self.kospi_200_midnsmall_.drop(['kospi_200_midnsmall_Open','kospi_200_midnsmall_High','kospi_200_midnsmall_Low','kospi_200_midnsmall_Volume'], axis=1)
        # 대표지수 (코스피 200 초대형제외 지수)
        self.kospi_200_exbig_ = stock.get_index_ohlcv_by_date(self.start_date__, self.end_date__, "1182")
        self.kospi_200_exbig_.columns = ['kospi_200_exbig_Open','kospi_200_exbig_High','kospi_200_exbig_Low','kospi_200_exbig_Close','kospi_200_exbig_Volume']
        self.kospi_200_exbig_ = self.kospi_200_exbig_.drop(['kospi_200_exbig_Open','kospi_200_exbig_High','kospi_200_exbig_Low','kospi_200_exbig_Volume'], axis=1)
        # 섹터지수 (코스피 200 커뮤니케이션 서비스)
        self.kospi_200_comm_ = stock.get_index_ohlcv_by_date(self.start_date__, self.end_date__, "1150")
        self.kospi_200_comm_.columns = ['kospi_200_comm_Open','kospi_200_comm_High','kospi_200_comm_Low','kospi_200_comm_Close','kospi_200_comm_Volume']
        self.kospi_200_comm_ = self.kospi_200_comm_.drop(['kospi_200_comm_Open','kospi_200_comm_High','kospi_200_comm_Low','kospi_200_comm_Volume'], axis=1)
        # 섹터지수 (코스피 200 건설)
        self.kospi_200_const_ = stock.get_index_ohlcv_by_date(self.start_date__, self.end_date__, "1151")
        self.kospi_200_const_.columns = ['kospi_200_const_Open','kospi_200_const_High','kospi_200_const_Low','kospi_200_const_Close','kospi_200_const_Volume']
        self.kospi_200_const_ = self.kospi_200_const_.drop(['kospi_200_const_Open','kospi_200_const_High','kospi_200_const_Low','kospi_200_const_Volume'], axis=1)
        # 섹터지수 (코스피 200 중공업)
        self.kospi_200_heavy_ = stock.get_index_ohlcv_by_date(self.start_date__, self.end_date__, "1152")
        self.kospi_200_heavy_.columns = ['kospi_200_heavy_Open','kospi_200_heavy_High','kospi_200_heavy_Low','kospi_200_heavy_Close','kospi_200_heavy_Volume']
        self.kospi_200_heavy_ = self.kospi_200_heavy_.drop(['kospi_200_heavy_Open','kospi_200_heavy_High','kospi_200_heavy_Low','kospi_200_heavy_Volume'], axis=1)
        # 섹터지수 (코스피 200 철강/소재)
        self.kospi_200_steel_ = stock.get_index_ohlcv_by_date(self.start_date__, self.end_date__, "1153")
        self.kospi_200_steel_.columns = ['kospi_200_steel_Open','kospi_200_steel_High','kospi_200_steel_Low','kospi_200_steel_Close','kospi_200_steel_Volume']
        self.kospi_200_steel_ = self.kospi_200_steel_.drop(['kospi_200_steel_Open','kospi_200_steel_High','kospi_200_steel_Low','kospi_200_steel_Volume'], axis=1)
        # 섹터지수 (코스피 200 에너지/화학)
        self.kospi_200_energy_ = stock.get_index_ohlcv_by_date(self.start_date__, self.end_date__, "1154")
        self.kospi_200_energy_.columns = ['kospi_200_energy_Open','kospi_200_energy_High','kospi_200_energy_Low','kospi_200_energy_Close','kospi_200_energy_Volume']
        self.kospi_200_energy_ = self.kospi_200_energy_.drop(['kospi_200_energy_Open','kospi_200_energy_High','kospi_200_energy_Low','kospi_200_energy_Volume'], axis=1)
        # 섹터지수 (코스피 200 정보기술)
        self.kospi_200_info_ = stock.get_index_ohlcv_by_date(self.start_date__, self.end_date__, "1155")
        self.kospi_200_info_.columns = ['kospi_200_info_Open','kospi_200_info_High','kospi_200_info_Low','kospi_200_info_Close','kospi_200_info_Volume']
        self.kospi_200_info_ = self.kospi_200_info_.drop(['kospi_200_info_Open','kospi_200_info_High','kospi_200_info_Low','kospi_200_info_Volume'], axis=1)
        # 섹터지수 (코스피 200 금융)
        self.kospi_200_finance_ = stock.get_index_ohlcv_by_date(self.start_date__, self.end_date__, "1156")
        self.kospi_200_finance_.columns = ['kospi_200_finance_Open','kospi_200_finance_High','kospi_200_finance_Low','kospi_200_finance_Close','kospi_200_finance_Volume']
        self.kospi_200_finance_ = self.kospi_200_finance_.drop(['kospi_200_finance_Open','kospi_200_finance_High','kospi_200_finance_Low','kospi_200_finance_Volume'], axis=1)
        # 섹터지수 (코스피 200 생활소비재)
        self.kospi_200_life_ = stock.get_index_ohlcv_by_date(self.start_date__, self.end_date__, "1157")
        self.kospi_200_life_.columns = ['kospi_200_life_Open','kospi_200_life_High','kospi_200_life_Low','kospi_200_life_Close','kospi_200_life_Volume']
        self.kospi_200_life_ = self.kospi_200_life_.drop(['kospi_200_life_Open','kospi_200_life_High','kospi_200_life_Low','kospi_200_life_Volume'], axis=1)
        # 섹터지수 (코스피 200 경기소비재)
        self.kospi_200_economy_ = stock.get_index_ohlcv_by_date(self.start_date__, self.end_date__, "1158")
        self.kospi_200_economy_.columns = ['kospi_200_economy_Open','kospi_200_economy_High','kospi_200_economy_Low','kospi_200_economy_Close','kospi_200_economy_Volume']
        self.kospi_200_economy_ = self.kospi_200_economy_.drop(['kospi_200_economy_Open','kospi_200_economy_High','kospi_200_economy_Low','kospi_200_economy_Volume'], axis=1)
        # 섹터지수 (코스피 200 산업재)
        self.kospi_200_industy_ = stock.get_index_ohlcv_by_date(self.start_date__, self.end_date__, "1159")
        self.kospi_200_industy_.columns = ['kospi_200_industy_Open','kospi_200_industy_High','kospi_200_industy_Low','kospi_200_industy_Close','kospi_200_industy_Volume']
        self.kospi_200_industy_ = self.kospi_200_industy_.drop(['kospi_200_industy_Open','kospi_200_industy_High','kospi_200_industy_Low','kospi_200_industy_Volume'], axis=1)
        # 섹터지수 (코스피 200 헬스케어)
        self.kospi_200_health_ = stock.get_index_ohlcv_by_date(self.start_date__, self.end_date__, "1160")
        self.kospi_200_health_.columns = ['kospi_200_health_Open','kospi_200_health_High','kospi_200_health_Low','kospi_200_health_Close','kospi_200_health_Volume']
        self.kospi_200_health_ = self.kospi_200_health_.drop(['kospi_200_health_Open','kospi_200_health_High','kospi_200_health_Low','kospi_200_health_Volume'], axis=1)

        # 3) 환율 데이터

        # 주요 3개국 대비 원 환율
        # 달러/원
        self.exchange_rate_usd_ = investpy.get_currency_cross_historical_data(currency_cross='USD/KRW', from_date=self.start_date_, to_date=self.end_date_)
        self.exchange_rate_usd_.columns = ['exchange_rate_usd_Open', 'exchange_rate_usd_High', 'exchange_rate_usd_Low', 'exchange_rate_usd_Close', 'exchange_rate_usd_Currency']
        self.exchange_rate_usd_ = self.exchange_rate_usd_.drop(['exchange_rate_usd_Open','exchange_rate_usd_High','exchange_rate_usd_Low','exchange_rate_usd_Currency'], axis=1)
        # 유로/원
        self.exchange_rate_eur_ = investpy.get_currency_cross_historical_data(currency_cross='EUR/KRW', from_date=self.start_date_, to_date=self.end_date_)
        self.exchange_rate_eur_.columns = ['exchange_rate_eur_Open', 'exchange_rate_eur_High', 'exchange_rate_eur_Low', 'exchange_rate_eur_Close', 'exchange_rate_eur_Currency']
        self.exchange_rate_eur_ = self.exchange_rate_eur_.drop(['exchange_rate_eur_Open','exchange_rate_eur_High','exchange_rate_eur_Low','exchange_rate_eur_Currency'], axis=1)
        # 엔/원
        self.exchange_rate_jpy_ = investpy.get_currency_cross_historical_data(currency_cross='JPY/KRW', from_date=self.start_date_, to_date=self.end_date_)
        self.exchange_rate_jpy_.columns = ['exchange_rate_jpy_Open', 'exchange_rate_jpy_High', 'exchange_rate_jpy_Low', 'exchange_rate_jpy_Close', 'exchange_rate_jpy_Currency']
        self.exchange_rate_jpy_ = self.exchange_rate_jpy_.drop(['exchange_rate_jpy_Open','exchange_rate_jpy_High','exchange_rate_jpy_Low','exchange_rate_jpy_Currency'], axis=1)
        # 위안/원
        self.exchange_rate_cny_ = investpy.get_currency_cross_historical_data(currency_cross='CNY/KRW', from_date=self.start_date_, to_date=self.end_date_)
        self.exchange_rate_cny_.columns = ['exchange_rate_cny_Open', 'exchange_rate_cny_High', 'exchange_rate_cny_Low', 'exchange_rate_cny_Close', 'exchange_rate_cny_Currency']
        self.exchange_rate_cny_ = self.exchange_rate_cny_.drop(['exchange_rate_cny_Open','exchange_rate_cny_High','exchange_rate_cny_Low','exchange_rate_cny_Currency'], axis=1)
        """
        # 호주 달러/원
        exchange_rate_aud_ = investpy.get_currency_cross_historical_data(currency_cross='AUD/KRW', from_date=self.start_date_, to_date=self.end_date_)
        exchange_rate_aud_.columns = ['exchange_rate_aud_Open', 'exchange_rate_aud_High', 'exchange_rate_aud_Low', 'exchange_rate_aud_Close', 'exchange_rate_aud_Currency']
        exchange_rate_aud_ = exchange_rate_aud_.drop(['exchange_rate_aud_Open','exchange_rate_aud_High','exchange_rate_aud_Low','exchange_rate_aud_Currency'], axis=1)
        # 캐나다 달러/원
        exchange_rate_cad_ = investpy.get_currency_cross_historical_data(currency_cross='CAD/KRW', from_date=self.start_date_, to_date=self.end_date_)
        exchange_rate_cad_.columns = ['exchange_rate_cad_Open', 'exchange_rate_cad_High', 'exchange_rate_cad_Low', 'exchange_rate_cad_Close', 'exchange_rate_cad_Currency']
        exchange_rate_cad_ = exchange_rate_cad_.drop(['exchange_rate_cad_Open','exchange_rate_cad_High','exchange_rate_cad_Low','exchange_rate_cad_Currency'], axis=1)
        # 스위스 프랑/원
        exchange_rate_chf_ = investpy.get_currency_cross_historical_data(currency_cross='CHF/KRW', from_date=self.start_date_, to_date=self.end_date_)
        exchange_rate_chf_.columns = ['exchange_rate_chf_Open', 'exchange_rate_chf_High', 'exchange_rate_chf_Low', 'exchange_rate_chf_Close', 'exchange_rate_chf_Currency']
        exchange_rate_chf_ = exchange_rate_chf_.drop(['exchange_rate_chf_Open','exchange_rate_chf_High','exchange_rate_chf_Low','exchange_rate_chf_Currency'], axis=1)
        # 파운드/원
        exchange_rate_gbp_ = investpy.get_currency_cross_historical_data(currency_cross='GBP/KRW', from_date=self.start_date_, to_date=self.end_date_)
        exchange_rate_gbp_.columns = ['exchange_rate_gbp_Open', 'exchange_rate_gbp_High', 'exchange_rate_gbp_Low', 'exchange_rate_gbp_Close', 'exchange_rate_gbp_Currency']
        exchange_rate_gbp_ = exchange_rate_gbp_.drop(['exchange_rate_gbp_Open','exchange_rate_gbp_High','exchange_rate_gbp_Low','exchange_rate_gbp_Currency'], axis=1)
        # 홍콩 달러/원
        exchange_rate_hkd_ = investpy.get_currency_cross_historical_data(currency_cross='HKD/KRW', from_date=self.start_date_, to_date=self.end_date_)
        exchange_rate_hkd_.columns = ['exchange_rate_hkd_Open', 'exchange_rate_hkd_High', 'exchange_rate_hkd_Low', 'exchange_rate_hkd_Close', 'exchange_rate_hkd_Currency']
        exchange_rate_hkd_ = exchange_rate_hkd_.drop(['exchange_rate_hkd_Open','exchange_rate_hkd_High','exchange_rate_hkd_Low','exchange_rate_hkd_Currency'], axis=1)
        # 인도네시아 루피아/원
        exchange_rate_idr_ = investpy.get_currency_cross_historical_data(currency_cross='IDR/KRW', from_date=self.start_date_, to_date=self.end_date_)
        exchange_rate_idr_.columns = ['exchange_rate_idr_Open', 'exchange_rate_idr_High', 'exchange_rate_idr_Low', 'exchange_rate_idr_Close', 'exchange_rate_idr_Currency']
        exchange_rate_idr_ = exchange_rate_idr_.drop(['exchange_rate_idr_Open','exchange_rate_idr_High','exchange_rate_idr_Low','exchange_rate_idr_Currency'], axis=1)
        # 인도 루피/원
        exchange_rate_inr_ = investpy.get_currency_cross_historical_data(currency_cross='INR/KRW', from_date=self.start_date_, to_date=self.end_date_)
        exchange_rate_inr_.columns = ['exchange_rate_inr_Open', 'exchange_rate_inr_High', 'exchange_rate_inr_Low', 'exchange_rate_inr_Close', 'exchange_rate_inr_Currency']
        exchange_rate_inr_ = exchange_rate_inr_.drop(['exchange_rate_inr_Open','exchange_rate_inr_High','exchange_rate_inr_Low','exchange_rate_inr_Currency'], axis=1)
        # 말레이시아 링깃/원
        exchange_rate_myr_ = investpy.get_currency_cross_historical_data(currency_cross='MYR/KRW', from_date=self.start_date_, to_date=self.end_date_)
        exchange_rate_myr_.columns = ['exchange_rate_myr_Open', 'exchange_rate_myr_High', 'exchange_rate_myr_Low', 'exchange_rate_myr_Close', 'exchange_rate_myr_Currency']
        exchange_rate_myr_ = exchange_rate_myr_.drop(['exchange_rate_myr_Open','exchange_rate_myr_High','exchange_rate_myr_Low','exchange_rate_myr_Currency'], axis=1)
        # 뉴질랜드 달러/원
        exchange_rate_nzd_ = investpy.get_currency_cross_historical_data(currency_cross='NZD/KRW', from_date=self.start_date_, to_date=self.end_date_)
        exchange_rate_nzd_.columns = ['exchange_rate_nzd_Open', 'exchange_rate_nzd_High', 'exchange_rate_nzd_Low', 'exchange_rate_nzd_Close', 'exchange_rate_nzd_Currency']
        exchange_rate_nzd_ = exchange_rate_nzd_.drop(['exchange_rate_nzd_Open','exchange_rate_nzd_High','exchange_rate_nzd_Low','exchange_rate_nzd_Currency'], axis=1)
        # 싱가폴 달러/원
        exchange_rate_sgd_ = investpy.get_currency_cross_historical_data(currency_cross='SGD/KRW', from_date=self.start_date_, to_date=self.end_date_)
        exchange_rate_sgd_.columns = ['exchange_rate_sgd_Open', 'exchange_rate_sgd_High', 'exchange_rate_sgd_Low', 'exchange_rate_sgd_Close', 'exchange_rate_sgd_Currency']
        exchange_rate_sgd_ = exchange_rate_sgd_.drop(['exchange_rate_sgd_Open','exchange_rate_sgd_High','exchange_rate_sgd_Low','exchange_rate_sgd_Currency'], axis=1)
        # 태국 바트/원
        exchange_rate_thb_ = investpy.get_currency_cross_historical_data(currency_cross='THB/KRW', from_date=self.start_date_, to_date=self.end_date_)
        exchange_rate_thb_.columns = ['exchange_rate_thb_Open', 'exchange_rate_thb_High', 'exchange_rate_thb_Low', 'exchange_rate_thb_Close', 'exchange_rate_thb_Currency']
        exchange_rate_thb_ = exchange_rate_thb_.drop(['exchange_rate_thb_Open','exchange_rate_thb_High','exchange_rate_thb_Low','exchange_rate_thb_Currency'], axis=1)
        # 대만 신타이비/원
        exchange_rate_twd_ = investpy.get_currency_cross_historical_data(currency_cross='TWD/KRW', from_date=self.start_date_, to_date=self.end_date_)
        exchange_rate_twd_.columns = ['exchange_rate_twd_Open', 'exchange_rate_twd_High', 'exchange_rate_twd_Low', 'exchange_rate_twd_Close', 'exchange_rate_twd_Currency']
        exchange_rate_twd_ = exchange_rate_twd_.drop(['exchange_rate_twd_Open','exchange_rate_twd_High','exchange_rate_twd_Low','exchange_rate_twd_Currency'], axis=1)
        # 남아프리카 란드/원
        exchange_rate_zar_ = investpy.get_currency_cross_historical_data(currency_cross='ZAR/KRW', from_date=self.start_date_, to_date=self.end_date_)
        exchange_rate_zar_.columns = ['exchange_rate_zar_Open', 'exchange_rate_zar_High', 'exchange_rate_zar_Low', 'exchange_rate_zar_Close', 'exchange_rate_zar_Currency']
        exchange_rate_zar_ = exchange_rate_zar_.drop(['exchange_rate_zar_Open','exchange_rate_zar_High','exchange_rate_zar_Low','exchange_rate_zar_Currency'], axis=1)
        # 디르함/원
        exchange_rate_aed_ = investpy.get_currency_cross_historical_data(currency_cross='AED/KRW', from_date=self.start_date_, to_date=self.end_date_)
        exchange_rate_aed_.columns = ['exchange_rate_aed_Open', 'exchange_rate_aed_High', 'exchange_rate_aed_Low', 'exchange_rate_aed_Close', 'exchange_rate_aed_Currency']
        exchange_rate_aed_ = exchange_rate_aed_.drop(['exchange_rate_aed_Open','exchange_rate_aed_High','exchange_rate_aed_Low','exchange_rate_aed_Currency'], axis=1)
        # 아르헨티나 페소/원
        exchange_rate_ars_ = investpy.get_currency_cross_historical_data(currency_cross='ARS/KRW', from_date=self.start_date_, to_date=self.end_date_)
        exchange_rate_ars_.columns = ['exchange_rate_ars_Open', 'exchange_rate_ars_High', 'exchange_rate_ars_Low', 'exchange_rate_ars_Close', 'exchange_rate_ars_Currency']
        exchange_rate_ars_ = exchange_rate_ars_.drop(['exchange_rate_ars_Open','exchange_rate_ars_High','exchange_rate_ars_Low','exchange_rate_ars_Currency'], axis=1)
        # 브라질 헤안/원
        exchange_rate_brl_ = investpy.get_currency_cross_historical_data(currency_cross='BRL/KRW', from_date=self.start_date_, to_date=self.end_date_)
        exchange_rate_brl_.columns = ['exchange_rate_brl_Open', 'exchange_rate_brl_High', 'exchange_rate_brl_Low', 'exchange_rate_brl_Close', 'exchange_rate_brl_Currency']
        exchange_rate_brl_ = exchange_rate_brl_.drop(['exchange_rate_brl_Open','exchange_rate_brl_High','exchange_rate_brl_Low','exchange_rate_brl_Currency'], axis=1)
        # 칠레 페소/원
        exchange_rate_clp_ = investpy.get_currency_cross_historical_data(currency_cross='CLP/KRW', from_date=self.start_date_, to_date=self.end_date_)
        exchange_rate_clp_.columns = ['exchange_rate_clp_Open', 'exchange_rate_clp_High', 'exchange_rate_clp_Low', 'exchange_rate_clp_Close', 'exchange_rate_clp_Currency']
        exchange_rate_clp_ = exchange_rate_clp_.drop(['exchange_rate_clp_Open','exchange_rate_clp_High','exchange_rate_clp_Low','exchange_rate_clp_Currency'], axis=1)
        # 덴마크 크로네/원
        exchange_rate_dkk_ = investpy.get_currency_cross_historical_data(currency_cross='DKK/KRW', from_date=self.start_date_, to_date=self.end_date_)
        exchange_rate_dkk_.columns = ['exchange_rate_dkk_Open', 'exchange_rate_dkk_High', 'exchange_rate_dkk_Low', 'exchange_rate_dkk_Close', 'exchange_rate_dkk_Currency']
        exchange_rate_dkk_ = exchange_rate_dkk_.drop(['exchange_rate_dkk_Open','exchange_rate_dkk_High','exchange_rate_dkk_Low','exchange_rate_dkk_Currency'], axis=1)
        # 헝가리 포린트/원
        exchange_rate_huf_ = investpy.get_currency_cross_historical_data(currency_cross='HUF/KRW', from_date=self.start_date_, to_date=self.end_date_)
        exchange_rate_huf_.columns = ['exchange_rate_huf_Open', 'exchange_rate_huf_High', 'exchange_rate_huf_Low', 'exchange_rate_huf_Close', 'exchange_rate_huf_Currency']
        exchange_rate_huf_ = exchange_rate_huf_.drop(['exchange_rate_huf_Open','exchange_rate_huf_High','exchange_rate_huf_Low','exchange_rate_huf_Currency'], axis=1)
        # 이스라엘 세켈/원
        exchange_rate_ils_ = investpy.get_currency_cross_historical_data(currency_cross='ILS/KRW', from_date=self.start_date_, to_date=self.end_date_)
        exchange_rate_ils_.columns = ['exchange_rate_ils_Open', 'exchange_rate_ils_High', 'exchange_rate_ils_Low', 'exchange_rate_ils_Close', 'exchange_rate_ils_Currency']
        exchange_rate_ils_ = exchange_rate_ils_.drop(['exchange_rate_ils_Open','exchange_rate_ils_High','exchange_rate_ils_Low','exchange_rate_ils_Currency'], axis=1)
        # 아이스랜드 크로나/원
        exchange_rate_isk_ = investpy.get_currency_cross_historical_data(currency_cross='ISK/KRW', from_date=self.start_date_, to_date=self.end_date_)
        exchange_rate_isk_.columns = ['exchange_rate_isk_Open', 'exchange_rate_isk_High', 'exchange_rate_isk_Low', 'exchange_rate_isk_Close', 'exchange_rate_isk_Currency']
        exchange_rate_isk_ = exchange_rate_isk_.drop(['exchange_rate_isk_Open','exchange_rate_isk_High','exchange_rate_isk_Low','exchange_rate_isk_Currency'], axis=1)
        # 멕시코 페소/원
        exchange_rate_mxn_ = investpy.get_currency_cross_historical_data(currency_cross='MXN/KRW', from_date=self.start_date_, to_date=self.end_date_)
        exchange_rate_mxn_.columns = ['exchange_rate_mxn_Open', 'exchange_rate_mxn_High', 'exchange_rate_mxn_Low', 'exchange_rate_mxn_Close', 'exchange_rate_mxn_Currency']
        exchange_rate_mxn_ = exchange_rate_mxn_.drop(['exchange_rate_mxn_Open','exchange_rate_mxn_High','exchange_rate_mxn_Low','exchange_rate_mxn_Currency'], axis=1)
        # 노르웨이 크로네/원
        exchange_rate_nok_ = investpy.get_currency_cross_historical_data(currency_cross='NOK/KRW', from_date=self.start_date_, to_date=self.end_date_)
        exchange_rate_nok_.columns = ['exchange_rate_nok_Open', 'exchange_rate_nok_High', 'exchange_rate_nok_Low', 'exchange_rate_nok_Close', 'exchange_rate_nok_Currency']
        exchange_rate_nok_ = exchange_rate_nok_.drop(['exchange_rate_nok_Open','exchange_rate_nok_High','exchange_rate_nok_Low','exchange_rate_nok_Currency'], axis=1)
        # 필리핀 페소/원
        exchange_rate_php_ = investpy.get_currency_cross_historical_data(currency_cross='PHP/KRW', from_date=self.start_date_, to_date=self.end_date_)
        exchange_rate_php_.columns = ['exchange_rate_php_Open', 'exchange_rate_php_High', 'exchange_rate_php_Low', 'exchange_rate_php_Close', 'exchange_rate_php_Currency']
        exchange_rate_php_ = exchange_rate_php_.drop(['exchange_rate_php_Open','exchange_rate_php_High','exchange_rate_php_Low','exchange_rate_php_Currency'], axis=1)
        # 파키스탄 루피/원
        exchange_rate_pkr_ = investpy.get_currency_cross_historical_data(currency_cross='PKR/KRW', from_date=self.start_date_, to_date=self.end_date_)
        exchange_rate_pkr_.columns = ['exchange_rate_pkr_Open', 'exchange_rate_pkr_High', 'exchange_rate_pkr_Low', 'exchange_rate_pkr_Close', 'exchange_rate_pkr_Currency']
        exchange_rate_pkr_ = exchange_rate_pkr_.drop(['exchange_rate_pkr_Open','exchange_rate_pkr_High','exchange_rate_pkr_Low','exchange_rate_pkr_Currency'], axis=1)
        # 폴란드 즈워티/원
        exchange_rate_pln_ = investpy.get_currency_cross_historical_data(currency_cross='PLN/KRW', from_date=self.start_date_, to_date=self.end_date_)
        exchange_rate_pln_.columns = ['exchange_rate_pln_Open', 'exchange_rate_pln_High', 'exchange_rate_pln_Low', 'exchange_rate_pln_Close', 'exchange_rate_pln_Currency']
        exchange_rate_pln_ = exchange_rate_pln_.drop(['exchange_rate_pln_Open','exchange_rate_pln_High','exchange_rate_pln_Low','exchange_rate_pln_Currency'], axis=1)
        # 러시아 루블/원
        exchange_rate_rub_ = investpy.get_currency_cross_historical_data(currency_cross='RUB/KRW', from_date=self.start_date_, to_date=self.end_date_)
        exchange_rate_rub_.columns = ['exchange_rate_rub_Open', 'exchange_rate_rub_High', 'exchange_rate_rub_Low', 'exchange_rate_rub_Close', 'exchange_rate_rub_Currency']
        exchange_rate_rub_ = exchange_rate_rub_.drop(['exchange_rate_rub_Open','exchange_rate_rub_High','exchange_rate_rub_Low','exchange_rate_rub_Currency'], axis=1)
        # 리얄/원
        exchange_rate_sar_ = investpy.get_currency_cross_historical_data(currency_cross='SAR/KRW', from_date=self.start_date_, to_date=self.end_date_)
        exchange_rate_sar_.columns = ['exchange_rate_sar_Open', 'exchange_rate_sar_High', 'exchange_rate_sar_Low', 'exchange_rate_sar_Close', 'exchange_rate_sar_Currency']
        exchange_rate_sar_ = exchange_rate_sar_.drop(['exchange_rate_sar_Open','exchange_rate_sar_High','exchange_rate_sar_Low','exchange_rate_sar_Currency'], axis=1)
        # 스웨덴 크로나/원
        exchange_rate_sek_ = investpy.get_currency_cross_historical_data(currency_cross='SEK/KRW', from_date=self.start_date_, to_date=self.end_date_)
        exchange_rate_sek_.columns = ['exchange_rate_sek_Open', 'exchange_rate_sek_High', 'exchange_rate_sek_Low', 'exchange_rate_sek_Close', 'exchange_rate_sek_Currency']
        exchange_rate_sek_ = exchange_rate_sek_.drop(['exchange_rate_sek_Open','exchange_rate_sek_High','exchange_rate_sek_Low','exchange_rate_sek_Currency'], axis=1)
        # 터키 리라/원
        exchange_rate_try_ = investpy.get_currency_cross_historical_data(currency_cross='TRY/KRW', from_date=self.start_date_, to_date=self.end_date_)
        exchange_rate_try_.columns = ['exchange_rate_try_Open', 'exchange_rate_try_High', 'exchange_rate_try_Low', 'exchange_rate_try_Close', 'exchange_rate_try_Currency']
        exchange_rate_try_ = exchange_rate_try_.drop(['exchange_rate_try_Open','exchange_rate_try_High','exchange_rate_try_Low','exchange_rate_try_Currency'], axis=1)
        """

        # 4) 원자재 데이터 (금값시세, 유가 등)
        # 금속
        # comex 금 시세
        self.comex_gold_ = yf.download("GC=F", start=self.start_date, end=self.end_date)
        self.comex_gold_.columns = ['comex_gold_Open','comex_gold_High','comex_gold_Low','comex_gold_Close','comex_gold_Adj Close','comex_gold_Volume']
        self.comex_gold_ = self.comex_gold_.drop(['comex_gold_Open','comex_gold_High','comex_gold_Low','comex_gold_Adj Close','comex_gold_Volume'], axis=1)
        # comex 미니 금 시세
        self.comex_mini_gold_ = yf.download("MGC=F", start=self.start_date, end=self.end_date)
        self.comex_mini_gold_.columns = ['comex_mini_gold_Open','comex_mini_gold_High','comex_mini_gold_Low','comex_mini_gold_Close','comex_mini_gold_Adj Close','comex_mini_gold_Volume']
        self.comex_mini_gold_ = self.comex_mini_gold_.drop(['comex_mini_gold_Open','comex_mini_gold_High','comex_mini_gold_Low','comex_mini_gold_Adj Close','comex_mini_gold_Volume'], axis=1)
        # comex 은 시세
        self.comex_silver_ = yf.download("SI=F", start=self.start_date, end=self.end_date)
        self.comex_silver_.columns = ['comex_silver_Open','comex_silver_High','comex_silver_Low','comex_silver_Close','comex_silver_Adj Close','comex_silver_Volume']
        self.comex_silver_ = self.comex_silver_.drop(['comex_silver_Open','comex_silver_High','comex_silver_Low','comex_silver_Adj Close','comex_silver_Volume'], axis=1)
        # comex 미니 은 시세
        self.comex_mini_silver_ = yf.download("SIL=F", start=self.start_date, end=self.end_date)
        self.comex_mini_silver_.columns = ['comex_mini_silver_Open','comex_mini_silver_High','comex_mini_silver_Low','comex_mini_silver_Close','comex_mini_silver_Adj Close','comex_mini_silver_Volume']
        self.comex_mini_silver_ = self.comex_mini_silver_.drop(['comex_mini_silver_Open','comex_mini_silver_High','comex_mini_silver_Low','comex_mini_silver_Adj Close','comex_mini_silver_Volume'], axis=1)
        # comex 동(구리) 시세
        self.comex_copper_ = yf.download("PL=F", start=self.start_date, end=self.end_date)
        self.comex_copper_.columns = ['comex_copper_Open','comex_copper_High','comex_copper_Low','comex_copper_Close','comex_copper_Adj Close','comex_copper_Volume']
        self.comex_copper_ = self.comex_copper_.drop(['comex_copper_Open','comex_copper_High','comex_copper_Low','comex_copper_Adj Close','comex_copper_Volume'], axis=1)
        # 미국 플래티넘 시세
        self.platinum_ = yf.download("HG=F", start=self.start_date, end=self.end_date)
        self.platinum_.columns = ['platinum_Open','platinum_High','platinum_Low','platinum_Close','platinum_Adj Close','platinum_Volume']
        self.platinum_ = self.platinum_.drop(['platinum_Open','platinum_High','platinum_Low','platinum_Adj Close','platinum_Volume'], axis=1)
        # 미국 팔라듐 시세
        self.palladium_ = yf.download("PA=F", start=self.start_date, end=self.end_date)
        self.palladium_.columns = ['palladium_Open','palladium_High','palladium_Low','palladium_Close','palladium_Adj Close','palladium_Volume']
        self.palladium_ = self.palladium_.drop(['palladium_Open','palladium_High','palladium_Low','palladium_Adj Close','palladium_Volume'], axis=1)

        # 에너지
        # WTI유 시세
        self.crude_oil_ = yf.download("CL=F", start=self.start_date, end=self.end_date)
        self.crude_oil_.columns = ['crude_oil_Open','crude_oil_High','crude_oil_Low','crude_oil_Close','crude_oil_Adj Close','crude_oil_Volume']
        self.crude_oil_ = self.crude_oil_.drop(['crude_oil_Open','crude_oil_High','crude_oil_Low','crude_oil_Adj Close','crude_oil_Volume'], axis=1)
        # 브렌트유 시세
        #brent_crude_oil_ = yf.download("BZ=F", start=self.start_date, end=self.end_date)
        #brent_crude_oil_.columns = ['brent_crude_oil_Open','brent_crude_oil_High','brent_crude_oil_Low','brent_crude_oil_Close','brent_crude_oil_Adj Close','brent_crude_oil_Volume']
        #brent_crude_oil_ = brent_crude_oil_.drop(['brent_crude_oil_Open','brent_crude_oil_High','brent_crude_oil_Low','brent_crude_oil_Adj Close','brent_crude_oil_Volume'], axis=1)
        # 가솔린 RBOB 시세
        self.rbob_gasoilne_ = yf.download("RB=F", start=self.start_date, end=self.end_date)
        self.rbob_gasoilne_.columns = ['rbob_gasoilne_Open','rbob_gasoilne_High','rbob_gasoilne_Low','rbob_gasoilne_Close','rbob_gasoilne_Adj Close','rbob_gasoilne_Volume']
        self.rbob_gasoilne_ = self.rbob_gasoilne_.drop(['rbob_gasoilne_Open','rbob_gasoilne_High','rbob_gasoilne_Low','rbob_gasoilne_Adj Close','rbob_gasoilne_Volume'], axis=1)
        # 미국 천연가스 시세
        self.natural_gas_ = yf.download("NG=F", start=self.start_date, end=self.end_date)
        self.natural_gas_.columns = ['natural_gas_Open','natural_gas_High','natural_gas_Low','natural_gas_Close','natural_gas_Adj Close','natural_gas_Volume']
        self.natural_gas_ = self.natural_gas_.drop(['natural_gas_Open','natural_gas_High','natural_gas_Low','natural_gas_Adj Close','natural_gas_Volume'], axis=1)
        # 미국 난방유 시세
        self.heating_oil_ = yf.download("HO=F", start=self.start_date, end=self.end_date)
        self.heating_oil_.columns = ['heating_oil_Open','heating_oil_High','heating_oil_Low','heating_oil_Close','heating_oil_Adj Close','heating_oil_Volume']
        self.heating_oil_ = self.heating_oil_.drop(['heating_oil_Open','heating_oil_High','heating_oil_Low','heating_oil_Adj Close','heating_oil_Volume'], axis=1)

        # 5) 금리 데이터
        # 미국 국채 수익률 (13주)
        self.treasury_13w_ = yf.download("^IRX", start=self.start_date, end=self.end_date)
        self.treasury_13w_.columns = ['treasury_13w_Open','treasury_13w_High','treasury_13w_Low','treasury_13w_Close','treasury_13w_Adj Close','treasury_13w_Volume']
        self.treasury_13w_ = self.treasury_13w_.drop(['treasury_13w_Open','treasury_13w_High','treasury_13w_Low','treasury_13w_Adj Close','treasury_13w_Volume'], axis=1)
        # 미국 국채 수익률 (5년)
        self.treasury_5y_ = yf.download("^FVX", start=self.start_date, end=self.end_date)
        self.treasury_5y_.columns = ['treasury_5y_Open','treasury_5y_High','treasury_5y_Low','treasury_5y_Close','treasury_5y_Adj Close','treasury_5y_Volume']
        self.treasury_5y_ = self.treasury_5y_.drop(['treasury_5y_Open','treasury_5y_High','treasury_5y_Low','treasury_5y_Adj Close','treasury_5y_Volume'], axis=1)
        # 미국 국채 수익률 (10년)
        self.treasury_10y_ = yf.download("^TNX", start=self.start_date, end=self.end_date)
        self.treasury_10y_.columns = ['treasury_10y_Open','treasury_10y_High','treasury_10y_Low','treasury_10y_Close','treasury_10y_Adj Close','treasury_10y_Volume']
        self.treasury_10y_ = self.treasury_10y_.drop(['treasury_10y_Open','treasury_10y_High','treasury_10y_Low','treasury_10y_Adj Close','treasury_10y_Volume'], axis=1)
        # 미국 국채 수익률 (30년)
        self.treasury_30y_ = yf.download("^TYX", start=self.start_date, end=self.end_date)
        self.treasury_30y_.columns = ['treasury_30y_Open','treasury_30y_High','treasury_30y_Low','treasury_30y_Close','treasury_30y_Adj Close','treasury_30y_Volume']
        self.treasury_30y_ = self.treasury_30y_.drop(['treasury_30y_Open','treasury_30y_High','treasury_30y_Low','treasury_30y_Adj Close','treasury_30y_Volume'], axis=1)

        # 한국 채권수익률 (지표수익률)
        self.kb = KrxBond()
        self.treasury_krx_ = self.kb.get_treasury_yields_in_bond_index(self.start_date__, self.end_date__).sort_index()
        self.treasury_krx_.columns = ['treasury_krx_3y','treasury_krx_5y','treasury_krx_10y','treasury_krx_20y','treasury_krx_30y']

        # 6) 글로벌 주가지수
        # Vix
        self.vix_ = yf.download("^VIX", start=self.start_date, end=self.end_date)
        self.vix_.columns = ['vix_Open','vix_High','vix_Low','vix_Close','vix_Adj Close','vix_Volume']
        self.vix_ = self.vix_.drop(['vix_Open','vix_High','vix_Low','vix_Adj Close','vix_Volume'], axis=1)
        # KOSPI Volatility
        self.vkospi_ = investpy.get_index_historical_data(index='KOSPI Volatility',country='South Korea', from_date=self.start_date_,to_date=self.end_date_)
        self.vkospi_.columns = ['vkospi_Open','vkospi_High','vkospi_Low','vkospi_Close','vkospi_Volume','vkospi_Currency']
        self.vkospi_ = self.vkospi_.drop(['vkospi_Open','vkospi_High','vkospi_Low','vkospi_Volume','vkospi_Currency'], axis=1)

        # Bitcoin USD
        self.bitcoin_ = yf.download("BTC-USD", start=self.start_date, end=self.end_date)
        self.bitcoin_.columns = ['bitcoin_Open','bitcoin_High','bitcoin_Low','bitcoin_Close','bitcoin_Adj Close','bitcoin_Volume']
        self.bitcoin_ = self.bitcoin_.drop(['bitcoin_Open','bitcoin_High','bitcoin_Low','bitcoin_Adj Close','bitcoin_Volume'], axis=1)

        # S&P 500
        self.snp_500_ = yf.download("^GSPC", start=self.start_date, end=self.end_date)
        self.snp_500_.columns = ['snp_500_Open','snp_500_High','snp_500_Low','snp_500_Close','snp_500_Adj Close','snp_500_Volume']
        self.snp_500_ = self.snp_500_.drop(['snp_500_Open','snp_500_High','snp_500_Low','snp_500_Adj Close','snp_500_Volume'], axis=1)
        # Dow Jones
        self.dow_jones_ = yf.download("^DJI", start=self.start_date, end=self.end_date)
        self.dow_jones_.columns = ['dow_jones_Open','dow_jones_High','dow_jones_Low','dow_jones_Close','dow_jones_Adj Close','dow_jones_Volume']
        self.dow_jones_ = self.dow_jones_.drop(['dow_jones_Open','dow_jones_High','dow_jones_Low','dow_jones_Adj Close','dow_jones_Volume'], axis=1)
        # NASDAQ
        self.nasdaq_ = yf.download("^IXIC", start=self.start_date, end=self.end_date)
        self.nasdaq_.columns = ['nasdaq_Open','nasdaq_High','nasdaq_Low','nasdaq_Close','nasdaq_Adj Close','nasdaq_Volume']
        self.nasdaq_ = self.nasdaq_.drop(['nasdaq_Open','nasdaq_High','nasdaq_Low','nasdaq_Adj Close','nasdaq_Volume'], axis=1)
        # NYSE
        self.nyse_ = yf.download("^NYA", start=self.start_date, end=self.end_date)
        self.nyse_.columns = ['nyse_Open','nyse_High','nyse_Low','nyse_Close','nyse_Adj Close','nyse_Volume']
        self.nyse_ = self.nyse_.drop(['nyse_Open','nyse_High','nyse_Low','nyse_Adj Close','nyse_Volume'], axis=1)
        # AMEX
        self.amex_ = yf.download("^XAX", start=self.start_date, end=self.end_date)
        self.amex_.columns = ['amex_Open','amex_High','amex_Low','amex_Close','amex_Adj Close','amex_Volume']
        self.amex_ = self.amex_.drop(['amex_Open','amex_High','amex_Low','amex_Adj Close','amex_Volume'], axis=1)

        # Russell 2000
        self.russell_2000_ = yf.download("^RUT", start=self.start_date, end=self.end_date)
        self.russell_2000_.columns = ['russell_2000_Open','russell_2000_High','russell_2000_Low','russell_2000_Close','russell_2000_Adj Close','russell_2000_Volume']
        self.russell_2000_ = self.russell_2000_.drop(['russell_2000_Open','russell_2000_High','russell_2000_Low','russell_2000_Adj Close','russell_2000_Volume'], axis=1)
        # DAX
        self.dax_ = yf.download("^GDAXI", start=self.start_date, end=self.end_date)
        self.dax_.columns = ['dax_Open','dax_High','dax_Low','dax_Close','dax_Adj Close','dax_Volume']
        self.dax_ = self.dax_.drop(['dax_Open','dax_High','dax_Low','dax_Adj Close','dax_Volume'], axis=1)
        # Nikkei 225
        self.nikkei_225_ = yf.download("^N225", start=self.start_date, end=self.end_date)
        self.nikkei_225_.columns = ['nikkei_225_Open','nikkei_225_High','nikkei_225_Low','nikkei_225_Close','nikkei_225_Adj Close','nikkei_225_Volume']
        self.nikkei_225_ = self.nikkei_225_.drop(['nikkei_225_Open','nikkei_225_High','nikkei_225_Low','nikkei_225_Adj Close','nikkei_225_Volume'], axis=1)
        # HANG SENG
        self.hang_seng_ = yf.download("^HSI", start=self.start_date, end=self.end_date)
        self.hang_seng_.columns = ['hang_seng_Open','hang_seng_High','hang_seng_Low','hang_seng_Close','hang_seng_Adj Close','hang_seng_Volume']
        self.hang_seng_ = self.hang_seng_.drop(['hang_seng_Open','hang_seng_High','hang_seng_Low','hang_seng_Adj Close','hang_seng_Volume'], axis=1)
        # SSE
        self.sse_ = yf.download("000001.SS", start=self.start_date, end=self.end_date)
        self.sse_.columns = ['sse_Open','sse_High','sse_Low','sse_Close','sse_Adj Close','sse_Volume']
        self.sse_ = self.sse_.drop(['sse_Open','sse_High','sse_Low','sse_Adj Close','sse_Volume'], axis=1)
        # ESTX 50
        self.estx_50_ = yf.download("^STOXX50E", start=self.start_date, end=self.end_date)
        self.estx_50_.columns = ['estx_50_Open','estx_50_High','estx_50_Low','estx_50_Close','estx_50_Adj Close','estx_50_Volume']
        self.estx_50_ = self.estx_50_.drop(['estx_50_Open','estx_50_High','estx_50_Low','estx_50_Adj Close','estx_50_Volume'], axis=1)
        # EURONEXT 100
        self.euronext_100_ = yf.download("^N100", start=self.start_date, end=self.end_date)
        self.euronext_100_.columns = ['euronext_100_Open','euronext_100_High','euronext_100_Low','euronext_100_Close','euronext_100_Adj Close','euronext_100_Volume']
        self.euronext_100_ = self.euronext_100_.drop(['euronext_100_Open','euronext_100_High','euronext_100_Low','euronext_100_Adj Close','euronext_100_Volume'], axis=1)

        # # 4. 데이터 전처리 (코스피지수 예측 모델)

        # 1) 예측 대상 설정
        self.model_kospi = self.kospi_.copy()

        # 2) 라벨링 (등락 여부, 동일 : 0, 상승 : 1, 하락 : 2)
        # kospi 모델
        self.lst_label = ['a']
        for i in range(len(self.model_kospi) - 1):
            if self.model_kospi.iloc[i + 1]['Close'] == self.model_kospi.iloc[i]['Close']:
                self.lst_label.append(0)  # 전일 주가 = 당일 주가 : 0
            elif self.model_kospi.iloc[i + 1]['Close'] > self.model_kospi.iloc[i]['Close']:
                self.lst_label.append(1)  # 전일 주가 < 당일 주가 : 1
            else:
                self.lst_label.append(2)  # 전일 주가 > 당일 주가 : 2
        self.model_kospi['Labeling'] = self.lst_label
        self.model_kospi = self.model_kospi.drop(self.model_kospi[self.model_kospi['Labeling'] == 'a'].index)  # 첫 행 삭제
        self.model_kospi = self.model_kospi.drop(self.model_kospi[self.model_kospi['Labeling'] == 0].index)  # 전일 주가 = 당일 주가인 행 삭제
        self.model_kospi['Labeling'] = self.model_kospi['Labeling'].astype("category")
        self.model_kospi = self.model_kospi.dropna()  # 결측치가 있는 행 제거

        # 3) 보조지표
        # 보조지표 추가
        # 1) 이평선(SMA, EMA, WMA) (w = 5,10,15,20,30,60,120)
        self.model_kospi['ma_5'] = ta.SMA(self.model_kospi.Close, timeperiod=5)
        self.model_kospi['ma_10'] = ta.SMA(self.model_kospi.Close, timeperiod=10)
        self.model_kospi['ma_15'] = ta.SMA(self.model_kospi.Close, timeperiod=15)
        self.model_kospi['ma_20'] = ta.SMA(self.model_kospi.Close, timeperiod=20)
        self.model_kospi['ma_30'] = ta.SMA(self.model_kospi.Close, timeperiod=30)
        self.model_kospi['ma_60'] = ta.SMA(self.model_kospi.Close, timeperiod=60)
        self.model_kospi['ma_120'] = ta.SMA(self.model_kospi.Close, timeperiod=120)

        self.model_kospi['ema_5'] = ta.EMA(self.model_kospi.Close, timeperiod=5)
        self.model_kospi['ema_10'] = ta.EMA(self.model_kospi.Close, timeperiod=10)
        self.model_kospi['ema_15'] = ta.EMA(self.model_kospi.Close, timeperiod=15)
        self.model_kospi['ema_20'] = ta.EMA(self.model_kospi.Close, timeperiod=20)
        self.model_kospi['ema_30'] = ta.EMA(self.model_kospi.Close, timeperiod=30)
        self.model_kospi['ema_60'] = ta.EMA(self.model_kospi.Close, timeperiod=60)
        self.model_kospi['ema_120'] = ta.EMA(self.model_kospi.Close, timeperiod=120)

        self.model_kospi['wma_5'] = ta.WMA(self.model_kospi.Close, timeperiod=5)
        self.model_kospi['wma_10'] = ta.WMA(self.model_kospi.Close, timeperiod=10)
        self.model_kospi['wma_15'] = ta.WMA(self.model_kospi.Close, timeperiod=15)
        self.model_kospi['wma_20'] = ta.WMA(self.model_kospi.Close, timeperiod=20)
        self.model_kospi['wma_30'] = ta.WMA(self.model_kospi.Close, timeperiod=30)
        self.model_kospi['wma_60'] = ta.WMA(self.model_kospi.Close, timeperiod=60)
        self.model_kospi['wma_120'] = ta.WMA(self.model_kospi.Close, timeperiod=120)

        self.model_kospi['ma_v5'] = ta.SMA(self.model_kospi.Volume, timeperiod=5)
        self.model_kospi['ma_v10'] = ta.SMA(self.model_kospi.Volume, timeperiod=10)
        self.model_kospi['ma_v20'] = ta.SMA(self.model_kospi.Volume, timeperiod=20)
        self.model_kospi['ma_v60'] = ta.SMA(self.model_kospi.Volume, timeperiod=60)
        self.model_kospi['ma_v120'] = ta.SMA(self.model_kospi.Volume, timeperiod=120)

        # 2) 볼린저밴드 (주가의 이동평균선을 중심으로 표준편차 범위를 표시)
        self.ubb, self.mbb, self.lbb = ta.BBANDS(self.model_kospi.Close, 20, 2)
        self.model_kospi['ubb'] = self.ubb
        self.model_kospi['mbb'] = self.mbb
        self.model_kospi['lbb'] = self.lbb

        # 3) MACD 이동평균수렴확산 (단기(EMA12)와 장기(EMA26) EMA로 모멘텀을 추정)
        self.macd, self.macdsignal9, self.macdhist = ta.MACD(self.model_kospi.Close, fastperiod=12, slowperiod=26, signalperiod=9)
        self.model_kospi['macd'] = self.macd
        self.model_kospi['macdsignal9'] = self.macdsignal9
        self.model_kospi['macdhist'] = self.macdhist

        # 4) RSI 상대강도지수 - 추세의 강도 파악, 과매수, 과매도 국면 판단
        self.model_kospi['rsi'] = ta.RSI(self.model_kospi.Close, timeperiod=14)

        # 5) 스토캐스틱 오늘의 주가가 일정 동안 주가의 변동폭 중에서 어느 정도인 지?
        self.slowk, self.slowd = ta.STOCH(self.model_kospi.High, self.model_kospi.Low, self.model_kospi.Close, fastk_period=5, slowk_period=3,
                                slowk_matype=0, slowd_period=3, slowd_matype=0)
        self.fastk, self.fastd = ta.STOCHF(self.model_kospi.High, self.model_kospi.Low, self.model_kospi.Close, fastk_period=5, fastd_period=3,
                                 fastd_matype=0)
        self.fastk_rsi, self.fastd_rsi = ta.STOCHRSI(self.model_kospi.Close, timeperiod=14, fastk_period=5, fastd_period=3,
                                           fastd_matype=0)
        self.model_kospi['slowk'] = self.slowk
        self.model_kospi['slowd'] = self.slowd
        self.model_kospi['fastk'] = self.fastk
        self.model_kospi['fastd'] = self.fastd
        self.model_kospi['fastk_rsi'] = self.fastk_rsi
        self.model_kospi['fastd_rsi'] = self.fastd_rsi

        # 6) 기타 자주 사용되는 것들
        # CCI (Commodity Channel Index), williams'%R, parabolic SAR
        # ADX (Average Directional Movement Index)
        # plusDI(Plus Directional Indicator), plusDM Plus Directional Movement)
        # ATR (Average True Range), OBV (On Balance Volume) 거래량 분석을 통한 주가분석, Variance
        self.model_kospi['cci'] = ta.CCI(self.model_kospi.High, self.model_kospi.Low, self.model_kospi.Close, timeperiod=14)
        self.model_kospi['willR'] = ta.WILLR(self.model_kospi.High, self.model_kospi.Low, self.model_kospi.Close, timeperiod=14)
        self.model_kospi['sar'] = ta.SAR(self.model_kospi.High, self.model_kospi.Low, acceleration=0, maximum=0)
        self.model_kospi['adx'] = ta.ADX(self.model_kospi.High, self.model_kospi.Low, self.model_kospi.Close, timeperiod=14)
        self.model_kospi['plus_di'] = ta.PLUS_DI(self.model_kospi.High, self.model_kospi.Low, self.model_kospi.Close, timeperiod=14)
        self.model_kospi['plus_dm'] = ta.PLUS_DM(self.model_kospi.High, self.model_kospi.Low, timeperiod=14)
        self.model_kospi['atr'] = ta.ATR(self.model_kospi.High, self.model_kospi.Low, self.model_kospi.Close, timeperiod=14)
        self.model_kospi['obv'] = ta.OBV(self.model_kospi.Close, self.model_kospi.Volume)
        self.model_kospi['var'] = ta.VAR(self.model_kospi.Close, timeperiod=5, nbdev=1)

        # 4) 분석 데이터 조합
        # 분석 데이터 병합
        self.model_kospi = pd.merge(self.model_kospi, self.kospi_short_sell_volume, how='inner', left_index=True, right_index=True)
        self.model_kospi = pd.merge(self.model_kospi, self.kospi_short_sell_value, how='inner', left_index=True, right_index=True)
        self.model_kospi = pd.merge(self.model_kospi, self.kospi_200_, how='inner', left_index=True, right_index=True)
        self.model_kospi = pd.merge(self.model_kospi, self.kospi_200_midnsmall_, how='inner', left_index=True, right_index=True)
        self.model_kospi = pd.merge(self.model_kospi, self.kospi_200_exbig_, how='inner', left_index=True, right_index=True)

        self.model_kospi = pd.merge(self.model_kospi, self.exchange_rate_usd_, how='inner', left_index=True, right_index=True)
        self.model_kospi = pd.merge(self.model_kospi, self.exchange_rate_eur_, how='inner', left_index=True, right_index=True)
        self.model_kospi = pd.merge(self.model_kospi, self.exchange_rate_jpy_, how='inner', left_index=True, right_index=True)
        self.model_kospi = pd.merge(self.model_kospi, self.exchange_rate_cny_, how='inner', left_index=True, right_index=True)

        self.model_kospi = pd.merge(self.model_kospi, self.comex_gold_, how='inner', left_index=True, right_index=True)
        self.model_kospi = pd.merge(self.model_kospi, self.comex_silver_, how='inner', left_index=True, right_index=True)
        self.model_kospi = pd.merge(self.model_kospi, self.comex_copper_, how='inner', left_index=True, right_index=True)
        self.model_kospi = pd.merge(self.model_kospi, self.platinum_, how='inner', left_index=True, right_index=True)
        self.model_kospi = pd.merge(self.model_kospi, self.palladium_, how='inner', left_index=True, right_index=True)

        self.model_kospi = pd.merge(self.model_kospi, self.crude_oil_, how='inner', left_index=True, right_index=True)
        self.model_kospi = pd.merge(self.model_kospi, self.rbob_gasoilne_, how='inner', left_index=True, right_index=True)
        self.model_kospi = pd.merge(self.model_kospi, self.natural_gas_, how='inner', left_index=True, right_index=True)
        self.model_kospi = pd.merge(self.model_kospi, self.heating_oil_, how='inner', left_index=True, right_index=True)

        self.model_kospi = pd.merge(self.model_kospi, self.treasury_13w_, how='inner', left_index=True, right_index=True)
        self.model_kospi = pd.merge(self.model_kospi, self.treasury_5y_, how='inner', left_index=True, right_index=True)
        self.model_kospi = pd.merge(self.model_kospi, self.treasury_10y_, how='inner', left_index=True, right_index=True)
        self.model_kospi = pd.merge(self.model_kospi, self.treasury_30y_, how='inner', left_index=True, right_index=True)
        self.model_kospi = pd.merge(self.model_kospi, self.treasury_krx_, how='inner', left_index=True, right_index=True)

        self.model_kospi = pd.merge(self.model_kospi, self.vix_, how='inner', left_index=True, right_index=True)
        self.model_kospi = pd.merge(self.model_kospi, self.bitcoin_, how='inner', left_index=True, right_index=True)
        self.model_kospi = pd.merge(self.model_kospi, self.snp_500_, how='inner', left_index=True, right_index=True)
        self.model_kospi = pd.merge(self.model_kospi, self.dow_jones_, how='inner', left_index=True, right_index=True)
        self.model_kospi = pd.merge(self.model_kospi, self.nasdaq_, how='inner', left_index=True, right_index=True)
        self.model_kospi = pd.merge(self.model_kospi, self.nyse_, how='inner', left_index=True, right_index=True)
        self.model_kospi = pd.merge(self.model_kospi, self.amex_, how='inner', left_index=True, right_index=True)

        self.scaling_col = [column for column in self.model_kospi.columns.difference(['Labeling'])]

        self.model_kospi = self.model_kospi.dropna()
        self.model_kospi = DataCollection.feature_scaling(self.model_kospi, scaling_strategy="z-score", column=self.scaling_col)
        #self.model_kospi.to_csv("model_kospi.csv", mode='w', index=False)

        self.cd = self.ed_date.strftime("%Y-%m-%d")
        self.ts = self.model_kospi.loc[self.cd]
        self.ms = self.model_kospi.append(self.ts, ignore_index=False)
        self.result_ = []
        self.result_.append(self.model_kospi)
        self.result_.append(self.ms.loc[self.cd])

        return self.result_


    # # 3. 데이터 수집 (와이지엔터 주가예측 모델)
    def yg_collection(self):
        # 1) 와이지엔터테인먼트 차트 데이터
        # 차트 데이터
        self.yg_ = stock.get_market_ohlcv_by_date(self.start_date__, self.end_date__, "122870")
        self.yg_.columns = ['Open','High','Low','Close','Volume']

        self.yg_market_cap = stock.get_market_cap_by_date(self.start_date__, self.end_date__, "122870")
        self.yg_market_cap.columns = ['Market_Value','Volume','Value','Num_Stock']
        del self.yg_market_cap['Volume']

        # 2) 와이지엔터테인먼트 투자지표
        # DIV/BPS/PER/EPS
        self.yg_fundamental = stock.get_market_fundamental_by_date(self.start_date__, self.end_date__, "122870")

        self.yg_short_sell = stock.get_shorting_status_by_date(self.start_date__, self.end_date__, "122870")
        self.yg_short_sell.columns = ['yg_short_sell','yg_balance','yg_short_sell_value','yg_balance_value']

        self.yg_short_sell_vol = stock.get_shorting_volume_by_date(self.start_date__, self.end_date__, "122870")
        self.yg_short_sell_vol.columns = ['yg_short_sell_volume','yg_total_volume', 'yg_short_sell_rate', 'yg_short_sell_value']


        # 3) 코스닥 주가지수 및 관련 투자지표
        # 종합지수 (코스닥) 차트 데이터
        self.kosdaq_ = stock.get_index_ohlcv_by_date(self.start_date__, self.end_date__, "2001")
        self.kosdaq_.columns = ['kosdaq_Open','kosdaq_High','kosdaq_Low','kosdaq_Close','kosdaq_Volume']

        # 코스닥 투자자별 공매도 거래량
        self.kosdaq_short_sell_volume = stock.get_shorting_investor_volume_by_date(self.start_date__, self.end_date__, "KOSDAQ")
        self.kosdaq_short_sell_volume.columns = ['kosdaq_inst_volume','kosdaq_indi_volume','kosdaq_fore_volume','kosdaq_etc_volume','kosdaq_short_sell_volume']
        # 코스닥 투자자별 공매도 거래대금
        self.kosdaq_short_sell_value = stock.get_shorting_investor_price_by_date(self.start_date__, self.end_date__, "KOSDAQ")
        self.kosdaq_short_sell_value.columns = ['kosdaq_inst_value','kosdaq_indi_value','kosdaq_fore_value','kosdaq_etc_value','kosdaq_short_sell_value']

        # 참고
        # 코스닥 항목별 시장 거래량
        #kosdaq_market_volume = stock.get_market_trading_volume_by_date(self.start_date__, self.end_date__, "KOSDAQ")
        # 코스닥 항목별 시장 거래대금
        #kosdaq_market_value = stock.get_market_trading_value_by_date(self.start_date__, self.end_date__, "KOSDAQ")

        # 대표지수 (코스닥 150)
        self.kosdaq_150 = stock.get_index_ohlcv_by_date(self.start_date__, self.end_date__, "2203")
        self.kosdaq_150.columns = ['kosdaq_150_Open','kosdaq_150_High','kosdaq_150_Low','kosdaq_150_Close','kosdaq_150_Volume']
        self.kosdaq_150 = self.kosdaq_150.drop(['kosdaq_150_Open','kosdaq_150_High','kosdaq_150_Low','kosdaq_150_Volume'], axis=1)
        # 섹터지수 (코스닥 150 커뮤니케이션서비스)
        self.kosdaq_150_comm = stock.get_index_ohlcv_by_date(self.start_date__, self.end_date__, "2218")
        self.kosdaq_150_comm.columns = ['kosdaq_150_comm_Open','kosdaq_150_comm_High','kosdaq_150_comm_Low','kosdaq_150_comm_Close','kosdaq_150_comm_Volume']
        self.kosdaq_150_comm = self.kosdaq_150_comm.drop(['kosdaq_150_comm_Open','kosdaq_150_comm_High','kosdaq_150_comm_Low','kosdaq_150_comm_Volume'], axis=1)
        # 산업별지수 (오락, 문화)
        self.kosdaq_enter = stock.get_index_ohlcv_by_date(self.start_date__, self.end_date__, "2037")
        self.kosdaq_enter.columns = ['kosdaq_enter_Open','kosdaq_enter_High','kosdaq_enter_Low','kosdaq_enter_Close','kosdaq_enter_Volume']
        self.kosdaq_enter = self.kosdaq_enter.drop(['kosdaq_enter_Open','kosdaq_enter_High','kosdaq_enter_Low','kosdaq_enter_Volume'], axis=1)
        # 시가총액 규모별 지수 (코스닥 대형주)
        self.kosdaq_large = stock.get_index_ohlcv_by_date(self.start_date__, self.end_date__, "2002")
        self.kosdaq_large.columns = ['kosdaq_large_Open','kosdaq_large_High','kosdaq_large_Low','kosdaq_large_Close','kosdaq_large_Volume']
        self.kosdaq_large = self.kosdaq_large.drop(['kosdaq_large_Open','kosdaq_large_High','kosdaq_large_Low','kosdaq_large_Volume'], axis=1)
        # 소속부 지수 (코스닥 우량기업부)
        self.kosdaq_super = stock.get_index_ohlcv_by_date(self.start_date__, self.end_date__, "2181")
        self.kosdaq_super.columns = ['kosdaq_super_Open','kosdaq_super_High','kosdaq_super_Low','kosdaq_super_Close','kosdaq_super_Volume']
        self.kosdaq_super = self.kosdaq_super.drop(['kosdaq_super_Open','kosdaq_super_High','kosdaq_super_Low','kosdaq_super_Volume'], axis=1)

        # # 5. 데이터 전처리 (와이지엔터 주가예측 모델)

        # 1) 예측 대상 설정
        self.model_yg = self.yg_.copy()

        # 2) 라벨링 (등락 여부, 동일 : 0, 상승 : 1, 하락 : 2)
        # yg 모델
        self.lst_label = ['a']
        for i in range(len(self.model_yg) - 1):
            if self.model_yg.iloc[i + 1]['Close'] == self.model_yg.iloc[i]['Close']:
                self.lst_label.append(0)  # 전일 주가 = 당일 주가 : 0
            elif self.model_yg.iloc[i + 1]['Close'] > self.model_yg.iloc[i]['Close']:
                self.lst_label.append(1)  # 전일 주가 < 당일 주가 : 1
            else:
                self.lst_label.append(2)  # 전일 주가 > 당일 주가 : 2
        self.model_yg['Labeling'] = self.lst_label
        self.model_yg = self.model_yg.drop(self.model_yg[self.model_yg['Labeling'] == 'a'].index)  # 첫 행 삭제
        self.model_yg = self.model_yg.drop(self.model_yg[self.model_yg['Labeling'] == 0].index)  # 전일 주가 = 당일 주가인 행 삭제
        self.model_yg['Labeling'] = self.model_yg['Labeling'].astype("category")
        self.model_yg = self.model_yg.dropna()  # 결측치가 있는 행 제거

        # 3) 보조지표
        # 보조지표 추가
        # 1) 이평선(SMA, EMA, WMA) (w = 5,10,15,20,30,60,120)
        self.model_yg['ma_5'] = ta.SMA(self.model_yg.Close, timeperiod=5)
        self.model_yg['ma_10'] = ta.SMA(self.model_yg.Close, timeperiod=10)
        self.model_yg['ma_15'] = ta.SMA(self.model_yg.Close, timeperiod=15)
        self.model_yg['ma_20'] = ta.SMA(self.model_yg.Close, timeperiod=20)
        self.model_yg['ma_30'] = ta.SMA(self.model_yg.Close, timeperiod=30)
        self.model_yg['ma_60'] = ta.SMA(self.model_yg.Close, timeperiod=60)
        self.model_yg['ma_120'] = ta.SMA(self.model_yg.Close, timeperiod=120)

        self.model_yg['ema_5'] = ta.EMA(self.model_yg.Close, timeperiod=5)
        self.model_yg['ema_10'] = ta.EMA(self.model_yg.Close, timeperiod=10)
        self.model_yg['ema_15'] = ta.EMA(self.model_yg.Close, timeperiod=15)
        self.model_yg['ema_20'] = ta.EMA(self.model_yg.Close, timeperiod=20)
        self.model_yg['ema_30'] = ta.EMA(self.model_yg.Close, timeperiod=30)
        self.model_yg['ema_60'] = ta.EMA(self.model_yg.Close, timeperiod=60)
        self.model_yg['ema_120'] = ta.EMA(self.model_yg.Close, timeperiod=120)

        self.model_yg['wma_5'] = ta.WMA(self.model_yg.Close, timeperiod=5)
        self.model_yg['wma_10'] = ta.WMA(self.model_yg.Close, timeperiod=10)
        self.model_yg['wma_15'] = ta.WMA(self.model_yg.Close, timeperiod=15)
        self.model_yg['wma_20'] = ta.WMA(self.model_yg.Close, timeperiod=20)
        self.model_yg['wma_30'] = ta.WMA(self.model_yg.Close, timeperiod=30)
        self.model_yg['wma_60'] = ta.WMA(self.model_yg.Close, timeperiod=60)
        self.model_yg['wma_120'] = ta.WMA(self.model_yg.Close, timeperiod=120)

        self.model_yg['ma_v5'] = ta.SMA(self.model_yg.Volume, timeperiod=5)
        self.model_yg['ma_v10'] = ta.SMA(self.model_yg.Volume, timeperiod=10)
        self.model_yg['ma_v20'] = ta.SMA(self.model_yg.Volume, timeperiod=20)
        self.model_yg['ma_v60'] = ta.SMA(self.model_yg.Volume, timeperiod=60)
        self.model_yg['ma_v120'] = ta.SMA(self.model_yg.Volume, timeperiod=120)

        # 2) 볼린저밴드 (주가의 이동평균선을 중심으로 표준편차 범위를 표시)
        self.ubb, self.mbb, self.lbb = ta.BBANDS(self.model_yg.Close, 20, 2)
        self.model_yg['ubb'] = self.ubb
        self.model_yg['mbb'] = self.mbb
        self.model_yg['lbb'] = self.lbb

        # 3) MACD 이동평균수렴확산 (단기(EMA12)와 장기(EMA26) EMA로 모멘텀을 추정)
        self.macd, self.macdsignal9, self.macdhist = ta.MACD(self.model_yg.Close, fastperiod=12, slowperiod=26, signalperiod=9)
        self.model_yg['macd'] = self.macd
        self.model_yg['macdsignal9'] = self.macdsignal9
        self.model_yg['macdhist'] = self.macdhist

        # 4) RSI 상대강도지수 - 추세의 강도 파악, 과매수, 과매도 국면 판단
        self.model_yg['rsi'] = ta.RSI(self.model_yg.Close, timeperiod=14)

        # 5) 스토캐스틱 오늘의 주가가 일정 동안 주가의 변동폭 중에서 어느 정도인 지?
        self.slowk, self.slowd = ta.STOCH(self.model_yg.High, self.model_yg.Low, self.model_yg.Close, fastk_period=5, slowk_period=3,
                                slowk_matype=0, slowd_period=3, slowd_matype=0)
        self.fastk, self.fastd = ta.STOCHF(self.model_yg.High, self.model_yg.Low, self.model_yg.Close, fastk_period=5, fastd_period=3,
                                 fastd_matype=0)
        self.fastk_rsi, self.fastd_rsi = ta.STOCHRSI(self.model_yg.Close, timeperiod=14, fastk_period=5, fastd_period=3,
                                           fastd_matype=0)
        self.model_yg['slowk'] = self.slowk
        self.model_yg['slowd'] = self.slowd
        self.model_yg['fastk'] = self.fastk
        self.model_yg['fastd'] = self.fastd
        self.model_yg['fastk_rsi'] = self.fastk_rsi
        self.model_yg['fastd_rsi'] = self.fastd_rsi

        # 6) 기타 자주 사용되는 것들
        # CCI (Commodity Channel Index), williams'%R, parabolic SAR
        # ADX (Average Directional Movement Index)
        # plusDI(Plus Directional Indicator), plusDM Plus Directional Movement)
        # ATR (Average True Range), OBV (On Balance Volume) 거래량 분석을 통한 주가분석, Variance
        self.model_yg['cci'] = ta.CCI(self.model_yg.High, self.model_yg.Low, self.model_yg.Close, timeperiod=14)
        self.model_yg['willR'] = ta.WILLR(self.model_yg.High, self.model_yg.Low, self.model_yg.Close, timeperiod=14)
        self.model_yg['sar'] = ta.SAR(self.model_yg.High, self.model_yg.Low, acceleration=0, maximum=0)
        self.model_yg['adx'] = ta.ADX(self.model_yg.High, self.model_yg.Low, self.model_yg.Close, timeperiod=14)
        self.model_yg['plus_di'] = ta.PLUS_DI(self.model_yg.High, self.model_yg.Low, self.model_yg.Close, timeperiod=14)
        self.model_yg['plus_dm'] = ta.PLUS_DM(self.model_yg.High, self.model_yg.Low, timeperiod=14)
        self.model_yg['atr'] = ta.ATR(self.model_yg.High, self.model_yg.Low, self.model_yg.Close, timeperiod=14)
        self.model_yg['obv'] = ta.OBV(self.model_yg.Close, self.model_yg.Volume)
        self.model_yg['var'] = ta.VAR(self.model_yg.Close, timeperiod=5, nbdev=1)

        # 4) 분석 데이터 병합 및 피쳐 스케일링
        # 분석 데이터 병합
        self.model_yg = pd.merge(self.model_yg, self.yg_market_cap, how='inner', left_index=True, right_index=True)
        self.model_yg = pd.merge(self.model_yg, self.yg_fundamental, how='inner', left_index=True, right_index=True)
        self.model_yg = pd.merge(self.model_yg, self.yg_short_sell, how='inner', left_index=True, right_index=True)
        self.model_yg = pd.merge(self.model_yg, self.yg_short_sell_vol, how='inner', left_index=True, right_index=True)
        self.model_yg = pd.merge(self.model_yg, self.kosdaq_short_sell_volume, how='inner', left_index=True, right_index=True)
        self.model_yg = pd.merge(self.model_yg, self.kosdaq_short_sell_value, how='inner', left_index=True, right_index=True)
        self.model_yg = pd.merge(self.model_yg, self.kosdaq_150, how='inner', left_index=True, right_index=True)
        self.model_yg = pd.merge(self.model_yg, self.kosdaq_150_comm, how='inner', left_index=True, right_index=True)
        self.model_yg = pd.merge(self.model_yg, self.kosdaq_enter, how='inner', left_index=True, right_index=True)
        self.model_yg = pd.merge(self.model_yg, self.kosdaq_large, how='inner', left_index=True, right_index=True)
        self.model_yg = pd.merge(self.model_yg, self.kosdaq_super, how='inner', left_index=True, right_index=True)

        self.scaling_col = [column for column in self.model_yg.columns.difference(['Labeling'])]

        self.model_yg = self.model_yg.dropna()
        self.model_yg = DataCollection.feature_scaling(self.model_yg, scaling_strategy="z-score", column=self.scaling_col)
        #self.model_yg.to_csv("model_yg.csv", mode='w', index=False)

        self.cd = self.ed_date.strftime("%Y-%m-%d")
        self.ts = self.model_yg.loc[self.cd]
        self.ms = self.model_yg.append(self.ts, ignore_index=False)
        self.result_ = []
        self.result_.append(self.model_yg)
        self.result_.append(self.ms.loc[self.cd])
        return self.result_


"""
# # 6. AutoML pycaret 모델

# 1) 예측 대상 설정

# 코스피 지수 예측 모델
train = model_kospi
# train = pd.read_csv('model_kospi.csv')

# 와이지엔터테인먼트 주가 예측 모델
# train = model_yg
# train = pd.read_csv('model_yg.csv')


# 2) 학습 모델 생성

# 분류 모델
clf = setup(data = train, target = 'Labeling', feature_selection = True, ignore_low_variance = True)

# 회귀 모델
#del train['Labeling']
#reg = setup(data = train, target = 'Close', feature_selection = True, ignore_low_variance = True)

best_3 = compare_models(n_select = 3)

blended = blend_models(estimator_list = best_3, fold = 5)

pred_holdout = predict_model(blended)

final_model = finalize_model(blended)

save_model(final_model, model_name = 'deployment_20201020')

"""
