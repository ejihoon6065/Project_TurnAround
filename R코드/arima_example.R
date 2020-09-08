install.packages("tseries")
install.packages("forecast")
install.packages("TTR")
library(tseries)
library(forecast)
library(TTR)

#https://stat-and-news-by-daragon9.tistory.com/47

king <- scan("https://robjhyndman.com/tsdldata/misc/kings.dat",skip=3)  # 1차원 데이터
print(class(king))

print(king)

king.ts<-ts(king)  # king : 1차원 데이터
print(class(king.ts))
plot.ts(king.ts)

king.sma3<-SMA(king.ts,n=3)    # 3년마다의 평균값
plot.ts(king.sma3)             # 3년 이평선


king.ff1<-diff(king.ts,differences = 1)  
plot.ts(king.ff1)

acf(king.ff1,lag.max=20)
acf(king.ff1,lag.max=20,plot=FALSE)

auto.arima(king)

# 영국 왕 사망시나이 시계열 자료의 적절한 모델을 ARIMA(0.1.1)모델에 FITTING(보정)
king.arima<-arima(king.ts,order=c(0,1,1))
king.arima

# Fitting후, forecast()함수를 이용해 미래 예측
king.forecasts<-forecast(king.arima)
king.forecasts

plot(king.forecasts)
