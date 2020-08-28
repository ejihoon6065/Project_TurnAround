# twitter_crawling
selenium을 이용한 트위터 크롤링


<코드 설명> 
- 사용자로 부터 검색 날짜와 키워드를 받아와서 크롤링한다.
- 크롤링 결과 : 날짜, 내용
- selenium 사용
- https://blog.naver.com/seodaeho91/221347214246 블로그 글 참고하고 만든 코드

<변경 사항>
- 만약 IndexError: list index out of range 에러가 뜬다면 코드 내의 모든 부분을 아래와 같이  변경할 것
-  변경 전=> date=soup.find_all("span",{"class": "_timestamp js-short-timestamp"})  
-  변경 후=> date=soup.find_all("span",{"class": "_timestamp js-short-timestamp "})  
