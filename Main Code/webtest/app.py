from pycaret.classification import load_model, predict_model
from pycaret.regression import *
import streamlit as st
import pandas as pd
import numpy as np
import copy
import DataCollectionModel
import ProphetModel
from fbprophet import Prophet # Prophet
from fbprophet.diagnostics import cross_validation # Prophet
from fbprophet.diagnostics import performance_metrics # Prophet
from fbprophet.plot import plot_cross_validation_metric # Prophet
from sklearn.metrics import *
from workalendar.asia import SouthKorea

# AutoML_CLA 예측 모델
def predict(model, input_df):
    predictions_df = predict_model(estimator=model, data=input_df)
    print(predictions_df)
    predictions = predictions_df['Label'][0]
    return predictions

# AutoML_REG 예측 모델
def predict_reg(model, input_df):
    data = copy.deepcopy(input_df[0])
    act_data = copy.deepcopy(input_df[2])
    del data['Labeling']
    del act_data['Labeling']
    predictions_df = predict_model(estimator=model, data=data)
    # 실제값
    actual_value = data.loc[act_data.index[-1]]['Close']
    # 예측값
    predict_value = predictions_df.loc[act_data.index[-1]]['Label']
    if actual_value < predict_value:
        return '1'
    else:
        return '0'

# 실행함수
def run():
    from PIL import Image
    image = Image.open('logo.jpg')
    image_stock = Image.open('stock.jpg')

    st.image(image, use_column_width=False)

    add_selectbox = st.sidebar.selectbox("예측 방법 결정",("Online", "Batch"))

    st.sidebar.info('프로젝트명 :' + '\n' + '자연어 처리 기반의 투자분석 및 예측시스템 개발')
    st.sidebar.success('★멘토님★ : 정좌연 PE')
    st.sidebar.info('팀명 : 턴어라운드')
    st.sidebar.success('팀원 : 이지훈, 이문형, 강민재, 구병진, 김서정')

    st.sidebar.image(image_stock)

    st.title("KOSPI 지수 및 YG 종목 주가 예측 모델")

    # 사용자 설정
    if add_selectbox == 'Online':
        date = str(st.number_input('Date', min_value=20200101, max_value=20201231, value=20201027))
        rev_date = date[0:4] + '-' + date[4:6] + '-' + date[6:]
        target = st.selectbox('Target', ['KOSPI', 'YG'])
        method = st.selectbox('Method', ['AutoML_CLA', 'AutoML_REG', 'ARIMA', 'Prophet', 'RL', 'NLP'])

        output = ""

        input_dict = {'Date': date, 'Target': target, 'Method': method}
        input_ = DataCollectionModel.DataCollection(date)
        prophet_input_ = ProphetModel.Prophet_(date)

        # 코스피 예측모델 데이터 수집 + 학습 데이터 준비
        if target == 'KOSPI':
            input_df = input_.kospi_collection()

            if method == 'AutoML_CLA':
                # 예측 모델
                model = load_model('deployment_kospi_20201029')
                # 학습 평가 모델
                model_train = load_model('deployment_kospi_train_20201029')
                load_test_model = predict_model(model_train, data=input_df[0].iloc[382:])
                test_model = load_test_model[['Labeling','Label']]

                acc_ = accuracy_score(test_model['Labeling'], test_model['Label'])
                auc_ = roc_auc_score(test_model['Labeling'], test_model['Label'])
                recall_ = recall_score(test_model['Labeling'], test_model['Label'])
                prec_ = precision_score(test_model['Labeling'], test_model['Label'])
                f1_ = f1_score(test_model['Labeling'], test_model['Label'])

                data = {'ACC': [acc_],
                        'AUC': [auc_],
                        'RECALL': [recall_],
                        'PREC': [prec_],
                        'F1': [f1_]}

                score_model = pd.DataFrame(data=data, columns=['ACC', 'AUC', 'RECALL', 'PREC', 'F1'])
                score_model.index.name = "Metrics Score"
                st.write("Test Data Metrics Score")
                st.table(score_model)

            elif method == 'AutoML_REG':

                # 예측 모델
                model = load_model('deployment_kospi_reg_20201029')
                # 학습 평가 모델
                model_train = load_model('deployment_kospi_reg_train_20201029')
                reg_data = copy.deepcopy(input_df[0].iloc[382:])
                del reg_data['Labeling']
                load_test_model = predict_model(model_train, data=reg_data)
                test_model = load_test_model[['Close', 'Label']]

                mae_ = mean_absolute_error(test_model['Close'], test_model['Label'])
                mse_ = mean_squared_error(test_model['Close'], test_model['Label'])
                rmse_ = mean_squared_error(test_model['Close'], test_model['Label'], squared=False)
                r2_ = r2_score(test_model['Close'], test_model['Label'])

                data = {'MAE': [mae_],
                        'MSE': [mse_],
                        'RMSE': [rmse_],
                        'R2': [r2_]}

                score_model = pd.DataFrame(data=data, columns=['MAE', 'MSE', 'RMSE', 'R2'])
                score_model.index.name = "Metrics Score"

                st.write("Test Data Metrics Score")
                st.table(score_model)
                st.write("Forecast Data (Test Data)")
                st.line_chart(test_model)

            elif method == 'ARIMA':
                # model load 필요시 여기에 추가
                print("ARIMA")

            elif method == 'Prophet':
                # model load 필요시 여기에 추가
                print("Prophet")

            elif method == 'RL':
                import main
                # model load 필요시 여기에 추가

                print("RL")

            elif method == 'NLP':
                # model load 필요시 여기에 추가
                print("NLP")

        # YG 예측모델 데이터 수집 + 학습 데이터 준비
        else:
            input_df = input_.yg_collection()

            if method == 'AutoML_CLA':
                # 예측 모델
                model = load_model('deployment_yg_20201029')
                # 학습 평가 모델
                model_train = load_model('deployment_yg_train_20201029')
                load_test_model = predict_model(model_train, data=input_df[0][341:])
                test_model = load_test_model[['Labeling', 'Label']]

                acc_ = accuracy_score(test_model['Labeling'], test_model['Label'])
                auc_ = roc_auc_score(test_model['Labeling'], test_model['Label'])
                recall_ = recall_score(test_model['Labeling'], test_model['Label'])
                prec_ = precision_score(test_model['Labeling'], test_model['Label'])
                f1_ = f1_score(test_model['Labeling'], test_model['Label'])

                data = {'ACC': [acc_],
                        'AUC': [auc_],
                        'RECALL': [recall_],
                        'PREC': [prec_],
                        'F1': [f1_]}

                score_model = pd.DataFrame(data=data, columns=['ACC', 'AUC', 'RECALL', 'PREC', 'F1'])
                score_model.index.name = "Metrics Score"
                st.write("Test Data Metrics Score")
                st.table(score_model)

            elif method == 'AutoML_REG':
                # 예측 모델
                model = load_model('deployment_yg_reg_20201029')
                # 학습 평가 모델
                model_train = load_model('deployment_yg_reg_train_20201029')
                reg_data = copy.deepcopy(input_df[0].iloc[341:])
                del reg_data['Labeling']
                load_test_model = predict_model(model_train, data=reg_data)
                test_model = load_test_model[['Close','Label']]

                mae_ = mean_absolute_error(test_model['Close'], test_model['Label'])
                mse_ = mean_squared_error(test_model['Close'], test_model['Label'])
                rmse_ = mean_squared_error(test_model['Close'], test_model['Label'], squared=False)
                r2_ = r2_score(test_model['Close'], test_model['Label'])

                data = {'MAE': [mae_],
                        'MSE': [mse_],
                        'RMSE': [rmse_],
                        'R2': [r2_]}

                score_model = pd.DataFrame(data=data, columns=['MAE', 'MSE', 'RMSE', 'R2'])
                score_model.index.name = "Metrics Score"

                st.write("Test Data Metrics Score")
                st.table(score_model)
                st.write("Forecast Data (Test Data)")
                st.line_chart(test_model)

            elif method == 'ARIMA':
                # model load 필요시 여기에 추가
                print("ARIMA")

            elif method == 'Prophet':
                # model load 필요시 여기에 추가
                print("prophet")

            elif method == 'RL':
                # model load 필요시 여기에 추가
                print("RL")

            elif method == 'NLP':
                print("NLP")

        # 예측 모델 실행
        buy_message = "주가 상승 예상 -> 매매 어드바이스 : 매수"
        sell_message = "주가 하락 예상 -> 매매 어드바이스 : 매도"

        if st.button("주가 예측"):
            if method == 'AutoML_CLA':
                output = predict(model=model, input_df=input_df[0])
                if output == '1':
                    output = date + buy_message
                else:
                    output = date + sell_message

            elif method == 'AutoML_REG':
                output = predict_reg(model=model, input_df=input_df)
                if output == '1':
                    output = date + buy_message
                else:
                    output = date + sell_message

            elif method == 'ARIMA':
                print("ARIMA")

            elif method == 'Prophet':
                if target == 'KOSPI':
                    df_prophet = copy.deepcopy(input_df[0])
                    df_prophet['date'] = pd.to_datetime(df_prophet.index)
                    df_data = df_prophet[['date', 'Close']].reset_index(drop=True)
                    df_data = df_data.rename(columns={'date': 'ds', 'Close': 'y'})

                    prop_model = Prophet(yearly_seasonality='auto',
                                         weekly_seasonality='auto',
                                         daily_seasonality='auto',
                                         changepoint_prior_scale=0.15,
                                         changepoint_range=0.9
                                         )

                    prop_model.add_country_holidays(country_name='KR')
                    prop_model.fit(df_data)

                    kor_holidays = pd.concat([pd.Series(np.array(SouthKorea().holidays(2020))[:, 0]),
                                              pd.Series(np.array(SouthKorea().holidays(2021))[:, 0])]).reset_index(
                        drop=True)

                    prop_future = prop_model.make_future_dataframe(periods=10)
                    prop_future = prop_future[prop_future.ds.dt.weekday != 5]
                    prop_future = prop_future[prop_future.ds.dt.weekday != 6]
                    for kor_holiday in kor_holidays:
                        prop_future = prop_future[prop_future.ds != kor_holiday]

                    prop_forecast = prop_model.predict(prop_future)
                    prop_forecast[['ds', 'yhat', 'yhat_upper', 'yhat_lower']]

                    fig1 = prop_model.plot(prop_forecast)
                    fig2 = prop_model.plot_components(prop_forecast)
                    #cv = cross_validation(prop_model, initial='10 days', period='20 days', horizon='5 days')
                    #df_pm = performance_metrics(cv)
                    #fig3 = plot_cross_validation_metric(cv, metric='rmse')

                    st.write("Forecast Data")
                    st.write(fig1)
                    st.write("Component Wise Forecast")
                    st.write(fig2)
                    #st.write("Cross Validation Metric")
                    #st.table(df_pm)
                    #st.write(fig3)
                    output = prophet_input_.prophet_kospi(input_df[0])

                    if output == '1':
                        output = date + buy_message
                    else:
                        output = date + sell_message
                else:
                    df_prophet = copy.deepcopy(input_df[0])
                    df_prophet['date'] = pd.to_datetime(df_prophet.index)
                    df_data = df_prophet[['date', 'Close']].reset_index(drop=True)
                    df_data = df_data.rename(columns={'date': 'ds', 'Close': 'y'})

                    # cp=['2019-10-23', '2019-11-04', '2019-11-13', '2019-11-22', '2019-12-04', '2019-12-13', '2019-12-26', '2020-01-08', '2020-01-17', '2020-01-31', '2020-02-11', '2020-02-20', '2020-03-03', '2020-03-12', '2020-03-23', '2020-04-02', '2020-04-13', '2020-04-23', '2020-05-08', '2020-05-19', '2020-05-29', '2020-06-09', '2020-06-18', '2020-06-30', '2020-07-09']
                    cp_spc = ['2020-08-11',
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

                    cp_default = ['2018-10-29',
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
                    cp = cp_default + cp_spc

                    prop_model = Prophet(yearly_seasonality='auto',
                                     weekly_seasonality='auto',
                                     daily_seasonality='auto',
                                     changepoints=cp,
                                     changepoint_range=0.85,
                                     changepoint_prior_scale=0.2
                                     )
                    prop_model.fit(df_data)
                    kor_holidays = pd.concat([pd.Series(np.array(SouthKorea().holidays(2019))[:, 0]),
                                                   pd.Series(np.array(SouthKorea().holidays(2020))[:, 0])]).reset_index(drop=True)
                    prop_future = prop_model.make_future_dataframe(periods=10)

                    prop_future = prop_future[prop_future.ds.dt.weekday != 5]
                    prop_future = prop_future[prop_future.ds.dt.weekday != 6]
                    for kor_holiday in kor_holidays:
                        prop_future = prop_future[prop_future.ds != kor_holiday]

                    prop_forecast = prop_model.predict(prop_future)
                    prop_forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(10)

                    fig1 = prop_model.plot(prop_forecast)
                    fig2 = prop_model.plot_components(prop_forecast)
                    #cv = cross_validation(prop_model, initial='10 days', period='20 days', horizon='5 days')
                    #df_pm = performance_metrics(cv)
                    #fig3 = plot_cross_validation_metric(cv, metric='rmse')

                    st.write("Forecast Data")
                    st.write(fig1)
                    st.write("Component Wise Forecast")
                    st.write(fig2)
                    #st.write("Cross Validation Metric")
                    #st.table(df_pm)
                    #st.write(fig3)
                    output = prophet_input_.prophet_yg(input_df[0])

                    if output == '1':
                        output = date + buy_message
                    else:
                        output = date + sell_message

        st.success(output)


    if add_selectbox == 'Batch':

        file_upload = st.file_uploader("Upload csv file for predictions", type=["csv"])

        if file_upload is not None:
            data = pd.read_csv(file_upload)
            predictions = predict_model(estimator=model, data=data)
            st.write(predictions)


if __name__ == '__main__':
    run()