from typing import Union

import pandas as pd
import numpy as np
import talib as ta

# COLUMNS_CHART_DATA = ['date', 'open', 'high', 'low', 'close', 'volume']
from pandas import DataFrame, Series

"""
COLUMNS_CHART_DATA = [
    'date', 'open', 'high', 'low', 'close', 'volume'
]
"""

COLUMNS_CHART_DATA = [
    'Date', 'Open', 'High', 'Low', 'Close', 'Volume'
]

COLUMNS_TRAINING_DATA_V1 = [
    'open_lastclose_ratio', 'high_close_ratio', 'low_close_ratio',
    'close_lastclose_ratio', 'volume_lastvolume_ratio',
    'close_ma5_ratio', 'volume_ma5_ratio',
    'close_ma10_ratio', 'volume_ma10_ratio',
    'close_ma20_ratio', 'volume_ma20_ratio',
    'close_ma60_ratio', 'volume_ma60_ratio',
    'close_ma120_ratio', 'volume_ma120_ratio',
]

COLUMNS_TRAINING_DATA_V1_RICH = [
    'open_lastclose_ratio', 'high_close_ratio', 'low_close_ratio',
    'close_lastclose_ratio', 'volume_lastvolume_ratio',
    'close_ma5_ratio', 'volume_ma5_ratio',
    'close_ma10_ratio', 'volume_ma10_ratio',
    'close_ma20_ratio', 'volume_ma20_ratio',
    'close_ma60_ratio', 'volume_ma60_ratio',
    'close_ma120_ratio', 'volume_ma120_ratio',
    'inst_lastinst_ratio', 'frgn_lastfrgn_ratio',
    'inst_ma5_ratio', 'frgn_ma5_ratio',
    'inst_ma10_ratio', 'frgn_ma10_ratio',
    'inst_ma20_ratio', 'frgn_ma20_ratio',
    'inst_ma60_ratio', 'frgn_ma60_ratio',
    'inst_ma120_ratio', 'frgn_ma120_ratio',
]

"""
COLUMNS_TRAINING_DATA_V2 = [
    'per', 'pbr', 'roe',
    'open_lastclose_ratio', 'high_close_ratio', 'low_close_ratio',
    'close_lastclose_ratio', 'volume_lastvolume_ratio',
    'close_ma5_ratio', 'volume_ma5_ratio',
    'close_ma10_ratio', 'volume_ma10_ratio',
    'close_ma20_ratio', 'volume_ma20_ratio',
    'close_ma60_ratio', 'volume_ma60_ratio',
    'close_ma120_ratio', 'volume_ma120_ratio',
    'market_kospi_ma5_ratio', 'market_kospi_ma20_ratio', 
    'market_kospi_ma60_ratio', 'market_kospi_ma120_ratio', 
    'bond_k3y_ma5_ratio', 'bond_k3y_ma20_ratio', 
    'bond_k3y_ma60_ratio', 'bond_k3y_ma120_ratio'
]
"""

# all feature
COLUMNS_TRAINING_DATA_V2 = [#'date', 'open', 'high', 'low', 'close', 'volume',
                            'value', 'stock_value',
                            'stock_volume', 'bps', 'pbr', 'dividend_per_stock', 'dividend_yield_ratio',
                            'volume_inst_buy', 'volume_inst_sell', 'volume_inst_pure_buy', 'volume_fore_buy',
                            'volume_fore_sell', 'volume_fore_pure_buy', 'value_inst_buy', 'value_inst_sell',
                            'value_inst_pure_buy', 'value_fore_buy', 'value_fore_sell', 'value_fore_pure_buy',
                            'kosdaq_close', 'kosdaq_open', 'kosdaq_high', 'kosdaq_low', 'kosdaq_volume', 'kosdaq_value',
                            'kosdaq_stock_value', 'kosdaq150_close', 'kosdaq150_open', 'kosdaq150_high', 'kosdaq150_low',
                            'kosdaq150_volume', 'kosdaq150_value', 'kosdaq150_stock_value', 'kosdaq150_comm_close', 'kosdaq150_comm_open',
                            'kosdaq150_comm_high', 'kosdaq150_comm_low', 'kosdaq150_comm_volume', 'kosdaq150_comm_value',
                            'kosdaq150_comm_stock_value', 'kosdaq_large_close', 'kosdaq_large_open', 'kosdaq_large_high',
                            'kosdaq_large_low', 'kosdaq_large_volume', 'kosdaq_large_value', 'kosdaq_large_stock_value',
                            'kosdaq_enter_close', 'kosdaq_enter_open', 'kosdaq_enter_high', 'kosdaq_enter_low', 'kosdaq_enter_volume',
                            'kosdaq_enter_value', 'kosdaq_stock_value.1', 'kosdaq_super_close', 'kosdaq_super_open', 'kosdaq_super_high',
                            'kosdaq_super_low', 'kosdaq_super_volume', 'kosdaq_super_value', 'kosdaq_super_stock_value',
                            'kosdaq_dividend_yield_ratio', 'kosdaq150_dividend_yield_ratio', 'kosdaq_large_dividend_yield_ratio',
                            'kosdaq_enter_dividend_yield_ratio', 'kosdaq_super_dividend_yield_ratio', 'kosdaq_per', 'kosdaq150_per',
                            'kosdaq_large_per', 'kosdaq_super_per', 'kosdaq_pbr', 'kosdaq150_pbr', 'kosdaq_large_pbr', 'kosdaq_enter_pbr',
                            'kosdaq_super_pbr', 'ma_5', 'ma_10', 'ma_15', 'ma_20', 'ma_30', 'ma_60', 'ma_120', 'ema_5', 'ema_10', 'ema_15',
                            'ema_20', 'ema_30', 'ema_60', 'ema_120', 'wma_5', 'wma_10', 'wma_15', 'wma_20', 'wma_30', 'wma_60', 'wma_120',
                            'ma_v5', 'ma_v10', 'ma_v20', 'ma_v60', 'ma_v120', 'ma_inst_v5', 'ma_inst_v10', 'ma_inst_v20', 'ma_inst_v60',
                            'ma_inst_v120', 'ma_fore_v5', 'ma_fore_v10', 'ma_fore_v20', 'ma_fore_v60', 'ma_fore_v120', 'ubb', 'mbb', 'lbb',
                            'macd', 'macdsignal9', 'macdhist', 'rsi', 'slowk', 'slowd', 'fastk', 'fastd', 'fastk_rsi', 'fastd_rsi', 'cci',
                            'willR', 'sar', 'adx', 'plus_di', 'plus_dm', 'atr', 'obv', 'var']

def preprocess(data, ver='v1'):
    windows = [5, 10, 20, 60, 120]
    for window in windows:
        data['close_ma{}'.format(window)] = \
            data['close'].rolling(window).mean()
        data['volume_ma{}'.format(window)] = \
            data['volume'].rolling(window).mean()
        data['close_ma%d_ratio' % window] = \
            (data['close'] - data['close_ma%d' % window]) \
            / data['close_ma%d' % window]
        data['volume_ma%d_ratio' % window] = \
            (data['volume'] - data['volume_ma%d' % window]) \
            / data['volume_ma%d' % window]
            
        if ver == 'v1.rich':
            data['inst_ma{}'.format(window)] = \
                data['close'].rolling(window).mean()
            data['frgn_ma{}'.format(window)] = \
                data['volume'].rolling(window).mean()
            data['inst_ma%d_ratio' % window] = \
                (data['close'] - data['inst_ma%d' % window]) \
                / data['inst_ma%d' % window]
            data['frgn_ma%d_ratio' % window] = \
                (data['volume'] - data['frgn_ma%d' % window]) \
                / data['frgn_ma%d' % window]

    data['open_lastclose_ratio'] = np.zeros(len(data))
    data.loc[1:, 'open_lastclose_ratio'] = \
        (data['open'][1:].values - data['close'][:-1].values) \
        / data['close'][:-1].values
    data['high_close_ratio'] = \
        (data['high'].values - data['close'].values) \
        / data['close'].values
    data['low_close_ratio'] = \
        (data['low'].values - data['close'].values) \
        / data['close'].values
    data['close_lastclose_ratio'] = np.zeros(len(data))
    data.loc[1:, 'close_lastclose_ratio'] = \
        (data['close'][1:].values - data['close'][:-1].values) \
        / data['close'][:-1].values
    data['volume_lastvolume_ratio'] = np.zeros(len(data))
    data.loc[1:, 'volume_lastvolume_ratio'] = \
        (data['volume'][1:].values - data['volume'][:-1].values) \
        / data['volume'][:-1] \
            .replace(to_replace=0, method='ffill') \
            .replace(to_replace=0, method='bfill').values

    if ver == 'v1.rich':
        data['inst_lastinst_ratio'] = np.zeros(len(data))
        data.loc[1:, 'inst_lastinst_ratio'] = \
            (data['inst'][1:].values - data['inst'][:-1].values) \
            / data['inst'][:-1] \
                .replace(to_replace=0, method='ffill') \
                .replace(to_replace=0, method='bfill').values
        data['frgn_lastfrgn_ratio'] = np.zeros(len(data))
        data.loc[1:, 'frgn_lastfrgn_ratio'] = \
            (data['frgn'][1:].values - data['frgn'][:-1].values) \
            / data['frgn'][:-1] \
                .replace(to_replace=0, method='ffill') \
                .replace(to_replace=0, method='bfill').values

    return data

def feature_scaling(df, scaling_strategy="min-max", column=None):
    if column == None:
        column = [column_name for column_name in df.columns]
    for column_name in column:
        if scaling_strategy == "min-max":
            df[column_name] = ( df[column_name] - df[column_name].min() ) / (df[column_name].max() - df[column_name].min())
        elif scaling_strategy == "z-score":
            df[column_name] = ( df[column_name] - df[column_name].mean() ) / (df[column_name].std() )
    return df

def preprocess_rev(data_4, ver='v2'):
    """
    # 액면분할 수정주가 반영영
    data_2 = data.iloc[:186]
    columns = ['close', 'open', 'high', 'low', 'eps', 'bps', 'dividend_per_stock']
    for column in columns:
        data_2[column] = data_2[column] / 5.0
    data_3 = data.iloc[189:]
    data_4 = pd.concat([data_2, data_3],axis=0)
    data_4 = data_4.dropna()
    """
    #
    del data_4['eps']
    del data_4['per']
    data_4 = data_4.dropna()
    # ['date_'] = data_4['date']
    data_4['open_'] = data_4['open']
    data_4['high_'] = data_4['high']
    data_4['low_'] = data_4['low']
    data_4['close_'] = data_4['close']
    data_4['volume_'] = data_4['volume']

    # 보조지표 추가
    # 1) 이평선(SMA, EMA, WMA) (w = 5,10,15,20,30,60,120)
    data_4['ma_5'] = ta.SMA(data_4.close, timeperiod=5)
    data_4['ma_10'] = ta.SMA(data_4.close, timeperiod=10)
    data_4['ma_15'] = ta.SMA(data_4.close, timeperiod=15)
    data_4['ma_20'] = ta.SMA(data_4.close, timeperiod=20)
    data_4['ma_30'] = ta.SMA(data_4.close, timeperiod=30)
    data_4['ma_60'] = ta.SMA(data_4.close, timeperiod=60)
    data_4['ma_120'] = ta.SMA(data_4.close, timeperiod=120)

    data_4['ema_5'] = ta.EMA(data_4.close, timeperiod=5)
    data_4['ema_10'] = ta.EMA(data_4.close, timeperiod=10)
    data_4['ema_15'] = ta.EMA(data_4.close, timeperiod=15)
    data_4['ema_20'] = ta.EMA(data_4.close, timeperiod=20)
    data_4['ema_30'] = ta.EMA(data_4.close, timeperiod=30)
    data_4['ema_60'] = ta.EMA(data_4.close, timeperiod=60)
    data_4['ema_120'] = ta.EMA(data_4.close, timeperiod=120)

    data_4['wma_5'] = ta.WMA(data_4.close, timeperiod=5)
    data_4['wma_10'] = ta.WMA(data_4.close, timeperiod=10)
    data_4['wma_15'] = ta.WMA(data_4.close, timeperiod=15)
    data_4['wma_20'] = ta.WMA(data_4.close, timeperiod=20)
    data_4['wma_30'] = ta.WMA(data_4.close, timeperiod=30)
    data_4['wma_60'] = ta.WMA(data_4.close, timeperiod=60)
    data_4['wma_120'] = ta.WMA(data_4.close, timeperiod=120)

    data_4['ma_v5'] = ta.SMA(data_4.volume, timeperiod=5)
    data_4['ma_v10'] = ta.SMA(data_4.volume, timeperiod=10)
    data_4['ma_v20'] = ta.SMA(data_4.volume, timeperiod=20)
    data_4['ma_v60'] = ta.SMA(data_4.volume, timeperiod=60)
    data_4['ma_v120'] = ta.SMA(data_4.volume, timeperiod=120)

    data_4['volume_inst_sub'] = data_4['volume_inst_buy'] - data_4['volume_inst_sell']
    data_4['volume_fore_sub'] = data_4['volume_fore_buy'] - data_4['volume_fore_sell']

    data_4['ma_inst_v5'] = ta.SMA(data_4.volume_inst_sub, timeperiod=5)
    data_4['ma_inst_v10'] = ta.SMA(data_4.volume_inst_sub, timeperiod=10)
    data_4['ma_inst_v20'] = ta.SMA(data_4.volume_inst_sub, timeperiod=20)
    data_4['ma_inst_v60'] = ta.SMA(data_4.volume_inst_sub, timeperiod=60)
    data_4['ma_inst_v120'] = ta.SMA(data_4.volume_inst_sub, timeperiod=120)

    data_4['ma_fore_v5'] = ta.SMA(data_4.volume_fore_sub, timeperiod=5)
    data_4['ma_fore_v10'] = ta.SMA(data_4.volume_fore_sub, timeperiod=10)
    data_4['ma_fore_v20'] = ta.SMA(data_4.volume_fore_sub, timeperiod=20)
    data_4['ma_fore_v60'] = ta.SMA(data_4.volume_fore_sub, timeperiod=60)
    data_4['ma_fore_v120'] = ta.SMA(data_4.volume_fore_sub, timeperiod=120)

    # 2) 볼린저밴드 (주가의 이동평균선을 중심으로 표준편차 범위를 표시)
    ubb, mbb, lbb = ta.BBANDS(data_4.close, 20, 2)
    data_4['ubb'] = ubb
    data_4['mbb'] = mbb
    data_4['lbb'] = lbb

    # 3) MACD 이동평균수렴확산 (단기(EMA12)와 장기(EMA26) EMA로 모멘텀을 추정)
    macd, macdsignal9, macdhist = ta.MACD(data_4.close, fastperiod=12, slowperiod=26, signalperiod=9)
    data_4['macd'] = macd
    data_4['macdsignal9'] = macdsignal9
    data_4['macdhist'] = macdhist

    # 4) RSI 상대강도지수 - 추세의 강도 파악, 과매수, 과매도 국면 판단
    data_4['rsi'] = ta.RSI(data_4.close, timeperiod=14)

    # 5) 스토캐스틱 오늘의 주가가 일정 동안 주가의 변동폭 중에서 어느 정도인 지?
    slowk, slowd = ta.STOCH(data_4.high, data_4.low, data_4.close, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
    fastk, fastd = ta.STOCHF(data_4.high, data_4.low, data_4.close, fastk_period=5, fastd_period=3, fastd_matype=0)
    fastk_rsi, fastd_rsi = ta.STOCHRSI(data_4.close, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
    data_4['slowk'] = slowk
    data_4['slowd'] = slowd
    data_4['fastk'] = fastk
    data_4['fastd'] = fastd
    data_4['fastk_rsi'] = fastk_rsi
    data_4['fastd_rsi'] = fastd_rsi

    # 6) 기타 자주 사용되는 것들
    # CCI (Commodity Channel Index), williams'%R, parabolic SAR
    # ADX (Average Directional Movement Index)
    # plusDI(Plus Directional Indicator), plusDM Plus Directional Movement)
    # ATR (Average True Range), OBV (On Balance Volume) 거래량 분석을 통한 주가분석, Variance
    data_4['cci'] = ta.CCI(data_4.high, data_4.low, data_4.close, timeperiod=14)
    data_4['willR'] = ta.WILLR(data_4.high, data_4.low, data_4.close, timeperiod=14)
    data_4['sar'] = ta.SAR(data_4.high, data_4.low, acceleration=0, maximum=0)
    data_4['adx'] = ta.ADX(data_4.high, data_4.low, data_4.close, timeperiod=14)
    data_4['plus_di'] = ta.PLUS_DI(data_4.high, data_4.low, data_4.close, timeperiod=14)
    data_4['plus_dm'] = ta.PLUS_DM(data_4.high, data_4.low, timeperiod=14)
    data_4['atr'] = ta.ATR(data_4.high, data_4.low, data_4.close, timeperiod=14)
    data_4['obv'] = ta.OBV(data_4.close, data_4.volume)
    data_4['var'] = ta.VAR(data_4.close, timeperiod=5, nbdev=1)

    # 7) Pattern REcognition
    # Investopedia "The 5 Most Powerful Candlestick Patterns"
    # Three Line Strike, Three Black Crows
    # Evening Star, Abandoned Baby
    # df4['line_str'] = ta.CDL3LINESTRIKE(df4.open, df4.high, df4.low, df4.close)
    # df4['blk_crw'] = ta.CDL3BLACKCROWS(df4.open, df4.high, df4.low, df4.close)
    # df4['evn_star'] = ta.CDLEVENINGSTAR(df4.open, df4.high, df4.low, df4.close, penetration=0)
    # df4['abn_baby'] = ta.CDLABANDONEDBABY(df4.open, df4.high, df4.low, df4.close, penetration=0)

    scaling_col = [column for column in data_4.columns]
    for i in range(6):
        scaling_col.pop(0)
    data_rev = data_4.copy()
    feature_scaling(data_rev, scaling_strategy="z-score", column=scaling_col)

    return data_rev

def load_data(fpath, date_from, date_to, ver='v2'):
    header = None if ver == 'v1' else 0
    data = pd.read_csv(fpath, thousands=',', header=header, 
        converters={'date': lambda x: str(x)})
    if ver == 'v1':
        data.columns = ['date', 'open', 'high', 'low', 'close', 'volume']

    # 데이터 전처리
    # data = preprocess(data)
    #data = preprocess_rev(data)
    # 기간 필터링
    data['Date'] = data['Date'].str.replace('-', '')
    data = data[(data['Date'] >= date_from) & (data['Date'] <= date_to)]
    data = data.dropna()

    # 차트 데이터 분리
    chart_data = data[COLUMNS_CHART_DATA]



    # 학습 데이터 분리
    training_data = None
    if ver == 'v1':
        training_data = data[COLUMNS_TRAINING_DATA_V1]
    elif ver == 'v1.rich':
        training_data = data[COLUMNS_TRAINING_DATA_V1_RICH]
    elif ver == 'v2':
        # data.loc[:, ['per', 'pbr', 'roe']] = \
            # data[['per', 'pbr', 'roe']].apply(lambda x: x / 100)
        training_data = data[data.columns.difference(COLUMNS_CHART_DATA)]
        training_data = training_data.apply(np.tanh)
    else:
        raise Exception('Invalid version.')
    
    return chart_data, training_data
