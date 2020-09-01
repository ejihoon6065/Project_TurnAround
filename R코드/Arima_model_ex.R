library(tseries)
library(forecast)
library(TTR)
install.packages("fpp2")
library(fpp2)
install.packages("ggplot2")
library(ggplot2)
install.packages("gridExtra")
library(gridExtra)
library(fpp2)
install.packages("TSA")

'''
A <- autoplot(AirPassengers, colour = "#00AFBB", size = 1.1) +
  geom_smooth(aes(y = AirPassengers), method = "lm", colour = "#FC4E07", formula = y ~ x + I(x^2), show.legend = TRUE)
A
# print(class(AirPassengers)) # autoplot()을 하려면 데이터타입이 ts여야함

'''


Sys.setlocale('LC_ALL','Korean')   # 한글 인코딩문제 해결
set.seed(123)

df<-read.csv("C:\\Users\\user\\Project_cslee_sj\\Project_TurnAround\\YG엔터주분석\\YG주가_2013_.csv",fileEncoding='UCS-2LE')
summary(df)

print(length(df$종가))  # 1880

df$날짜=as.POSIXlt(df$날짜,format = "%Y-%m-%d")  # df의 날짜속성(character형)을 datetime으로 바꾸어줌
  
'''
par(mfrow=c(1,1))
df$날짜 <- as.Date(df$날짜, "%Y-%m-%d")
axis(1, df$날짜, format(df$날짜, "%b %d"), cex.axis = .7)
plot(df$날짜, df$종가, xaxt = "n", type = "l")
'''

test_df<-data.frame(date=c(df$날짜),stock=c(df$종가))  # 날짜와 종가만 
print(head(test_df))

#plot(test_df$date,test_df$stock)

par(mfrow=c(1,1))
plot(df$날짜,df$종가,type='l')
df_dt<-test_df$date
df_st<-ts(test_df$stock)


par(mfrow=c(2,2))
plot(df_dt,df_st, type='l',main='YG주가')
plot(diff(df_st),type='l', main='YG주가에 차분적용')
plot(df_dt,log(df_st),type='l',main='YG주가에 로그' )
plot(diff(log(df_st)),type='l',main='YG주가에 로그후 차분적용')


par(mfrow=c(2,2))
plot(df_dt,df_st, type='l',main='YG주가',xlab='2013~2020',ylab='주가')
plot(df_dt[-1],diff(df_st),type='l', main='YG주가에 차분적용',xlab='2013~2020')
plot(df_dt,log(df_st),type='l',main='YG주가에 로그',xlab='2013~2020')
plot(df_dt[-1],diff(log(df_st)),type='l',main='YG주가에 로그후 차분적용',xlab='2013~2020')



par(mfrow=c(1,1))
dev.new(width=5, height=4)
plot(df_dt[-1],diff(df_st),type='l', main='YG주가에 차분적용',xlab='2013~2020')


par(mfrow=c(1,1))
dev.new(width=5, height=4)
plot(df_dt[-1],diff(log(df_st)),type='l',main='YG주가에 로그후 차분적용',xlab='2013~2020')

# 융-박스(Ljung-Box)  Q통계 

Box.test(diff(df_st), lag=10, type="Ljung-Box") 
# X-squared = 20.145, df = 10, p-value=0.02791

# 비정상적인 평균확인 (Original version)
par(oma=c(0,0,5,0))
par(mfrow = c(1,2))
acf(df_st , main="ACF", ylab="")
pacf(df_st, main="PACF", ylab="")
mtext("ACF, PACF of YG's Stock",outer=TRUE,cex=2)

adf.test(df_st, k=0)

# 정상성확인 _ 차분

par(oma=c(0,0,5,0))
par(mfrow = c(1,2))
acf(diff(df_st) , main="ACF", ylab="")
pacf(diff(df_st), main="PACF", ylab="")
mtext("DIFF()-ACF, PACF of YG's Stock",outer=TRUE,cex=2)

adf.test(diff(df_st), k=0)


# 정상성확인 _ 차분,로그

par(oma=c(0,0,5,0))
par(mfrow = c(1,2))
acf(diff(log(df_st)) , main="ACF", ylab="")
pacf(diff(log(df_st)), main="PACF", ylab="")
mtext("DIFF(),LOG() -ACF, PACF of YG's Stock",outer=TRUE,cex=2)

adf.test(diff(log(df_st)), k=9)


auto.arima(diff(log(df_st)))

