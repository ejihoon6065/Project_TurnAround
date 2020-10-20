from pycaret.classification import load_model, predict_model
import streamlit as st
import pandas as pd
import numpy as np
import DataCollectionModel
import ProphetModel

# AutoML 예측
def predict(model, input_df):
    predictions_df = predict_model(estimator=model, data=input_df)
    predictions = predictions_df['Label'][0]
    return predictions

# 실행함수
def run():
    from PIL import Image
    image = Image.open('logo.jpg')
    image_stock = Image.open('stock.jpg')

    st.image(image, use_column_width=False)

    add_selectbox = st.sidebar.selectbox("예측 방법 결정",("Online", "Batch"))

    st.sidebar.info('프로젝트명 :' + '\n' + '자연어 처리 기반의 투자분석 및 예측시스템 개발')
    st.sidebar.success('팀명 : 턴어라운드')
    st.sidebar.success('팀원 : 이지훈, 이문형, 강민재, 구병진, 김서정')

    st.sidebar.image(image_stock)

    st.title("코스피 지수 예측 모델")

    # 사용자 설정
    if add_selectbox == 'Online':
        date = str(st.number_input('Date', min_value=20200101, max_value=20201231, value=20201006))
        target = st.selectbox('Target', ['KOSPI', 'YG'])
        method = st.selectbox('Method', ['AutoML', 'ARIMA', 'Prophet', 'RL', 'NLP'])

        output = ""

        input_dict = {'Date': date, 'Target': target, 'Method': method}
        input_ = DataCollectionModel.DataCollection(date)
        prophet_input_ = ProphetModel.Prophet_(date)

        # 데이터 수집 + 학습 데이터 준비
        if target == 'KOSPI':
            input_df = input_.kospi_collection()
            if method == 'AutoML':
                model = load_model('deployment_20201020')
            elif method == 'Prophet':
                # model load 필요시 여기에 추가
                print("prophet")
        else:
            input_df = input_.yg_collection()
            if method == 'AutoML':
                model = load_model('deployment_yg_20201020')

        # 주가 예측
        if st.button("주가 예측"):
            if method == 'AutoML':
                output = predict(model=model, input_df=input_df[1])
                if output == '1':
                    output = date + "주가 상승 예상 -> 매매 어드바이스 : 매수"
                else:
                    output = date + "주가 하락 예상 -> 매매 어드바이스 : 매도"

            elif method == 'Prophet':
                if target == 'KOSPI':
                    output = prophet_input_.prophet_kospi(input_df[0])
                    if output == '1':
                        output = date + "주가 상승 예상 -> 매매 어드바이스 : 매수"
                    else:
                        output = date + "주가 하락 예상 -> 매매 어드바이스 : 매도"
                else:
                    output = prophet_input_.prophet_yg(input_df[0])
                    if output == '1':
                        output = date + "주가 상승 예상 -> 매매 어드바이스 : 매수"
                    else:
                        output = date + "주가 하락 예상 -> 매매 어드바이스 : 매도"

        st.success(output)


    if add_selectbox == 'Batch':

        file_upload = st.file_uploader("Upload csv file for predictions", type=["csv"])

        if file_upload is not None:
            data = pd.read_csv(file_upload)
            predictions = predict_model(estimator=model, data=data)
            st.write(predictions)


if __name__ == '__main__':
    run()