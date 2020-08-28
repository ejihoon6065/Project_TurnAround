if(!require(twitteR)) {install.packages("twitteR");library(twitteR)}

library(plyr)

api_key <- "R5VrST0NItNiVXt4j0EM61pfh"
api_secret <- "N7RX21JDSWaLtgdHKoy9i5qgTTK8oH051023mggNC2R8HTNzAJ"
access_token <- "353645141-LbAgUCRWEqVmfwQ3hFKoMYEk6c9rPLQRWqJNOF9G"
access_secret <- "lksmpYFIxEzDVqHQi2Orfuoomx0zg66Lx3fUSIkWGBOeA"

setup_twitter_oauth(api_key,api_secret,access_token,access_secret)

keyword <- enc2utf8("삼성")

tweets <- searchTwitter(keyword,n=1000,lang="ko") 
length(tweets)
temp <- tweets[[1]]
temp$getScreenName() # 사용자 이름 
temp$getText() # 화면상에 표시되는 아이디 


class(tweets)
tweets.text <- laply(tweets,function(t) t$getText())
length(tweets.text)
head(tweets.text,100)
