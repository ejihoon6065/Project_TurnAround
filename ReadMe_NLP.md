# 1) Konlpy 설치

## JAVA 설치
``` python
 1-1. JDK를 1.7 버전 이상으로 설치 (설치시, 경로를 기억해둡니다) (https://www.oracle.com/technetwork/java/javase/downloads/index.html)

 1-2. 윈도우10기준, 제어판 > 시스템 및 보안 > 시스템 > 고급 시스템 설정 > 고급 > 환경 변수에서 새로 만들기를 누르고 JAVA_HOME이라는 환경변수 생성 (환경변수값은 jdk설치경로)
      (*https://d2fault.github.io/2018/07/11/20180711-install-jdk-at-windows10/ 참고)

 1-3. J-Pype 설치(JAVA와 Python을 연결해주는 역할)
      설치주소 : https://www.lfd.uci.edu/~gohlke/pythonlibs/#jpype <- 해당주소에서 파이썬 버젼과 윈도우 OS비트수를 확인하여 다운로드
                                                                     (ex. 파이썬 3.7, 윈도우64비트 -> cp37..amd64.whl 다운)
                                                                     *파이썬 버전확인 : anaconda prompt 또는 CMD창에 “python --version” 이라 입력

 1-4. 프롬프트(CMD or Anaconda Prompt)에서 다운받은 파일의 경로로 이동하여 아래 커맨드를 통해 설치
      pip install JPype1‑0.6.3‑cp37‑cp37m‑win_amd64.whl

 2. from konlpy.tag import [원하는 형태소분석기] (형태소분석기 : Hannanum, Kkma, Komoran, Okt, Mecab)
    *Mecab은 아래에 추가 설정 필요
```


# 2) Mecab 설치

1. mecab-ko-msvc 설치하기 (‘C 기반으로 만들어진 mecab’이 윈도우에서 실행될 수 있도록 하는 역할)
``` python
(https://github.com/Pusnow/mecab-ko-msvc/releases/tag/release-0.9.2-msvc-3) 참고

 1-1. 윈도우 버전에 따라 32bit / 64bit 선택 다운로드

 1-2. ‘C 드라이브’에 mecab폴더 만들기 => “C:/mecab”

 1-3. ‘1-1’에서 다운로드 받은 ‘mecab-ko-msvc-x64.zip’ 또는 ‘mecab-ko-msvc-x84.zip’ 압축 풀기
```

2. mecab-ko-dic-msvc.zip 기본 사전 설치하기
``` python 
 2-1.사전 다운로드 ‘mecab-ko-dic-msvc.zip’
 https://github.com/Pusnow/mecab-ko-dic-msvc/releases/tag/mecab-ko-dic-2.1.1-20180720-msvc
 
 2-2. 앞서 ‘1-3’에서 만들었던 ‘C:/mecab’에 압축 해제
 * mecab 하위 폴더에 대강 파일들이 존재해야 함
```

3. python wheel 설치하기
``` python
 3-1. 링크 클릭
 https://github.com/Pusnow/mecab-python-msvc/releases/tag/mecab_python-0.996_ko_0.9.2_msvc-2

 3-2. 파이썬 및 윈도우 버전에 맞는 whl 다운로드
 ex. 윈도우 64bit에 파이썬 3.7인 경우, ‘mecab_python-0.996_ko_0.9.2_msvc-cp37-cp37m-win_amd64.whl’ 다운로드

 3-3. 다운로드 받은 파일을 site-package 폴더 안에 옮기기

 3-4. python 사용자의 경우 cmd창에서 site-package 폴더로 이동하여

‘pip install mecab_python-0.996_ko_0.9.2_msvc-cp37-cp37m-win_amd64.whl’
 pip install 다운로드받은파일명.whl’
 입력하여 설치 완료
```

4. mecab 사용자 사전 추가하기
``` python
 4-1. 사전 추가
 C:/mecab/user-dic 폴더에서 csv파일 3개를 확인할 수 있음
 이때, 명사는 nnp에, 인명은 person에, 지명은 place 파일에 각각 입력. 단, 제공하는 형식에 따를 것
 사전의 형식은 표층형/0/0/0/품사태그/의미분류/종성유무/읽기/타입/첫번째품사/마지막품사/표현 으로 구성

 4-2. 사전 컴파일
 윈도우 환경에서 Powershell을 활용하여 관리자 모드로 진행
 파워쉘이 구동되면 C:/mecab 폴더로 이동후(절대주소) tool 폴더에 있는 add-userdic-win.ps1을 실행
 단, 에러가 발생될 수 있음. 즉, UnauthorizedAccess 에러가 발생할 수 있는데 이때는 스크립트 실행 제한을 풀어줘야 함
 제한이 걸려있는지 확인하기 위해서 ExecutionPolicy를 입력하면 'Restricted'라고 나올 것이다.
 이 경우, 다시 ExecutionPolicy를 실행하면 'Unrestricted'라고 나오는 것을 확인할 수 있다.
 이제 tool 폴더에 있는 add-user-dic-win.ps1을 실행
 'done!'이라는 것이 나타나면 사전 컴파일이 완료된 것임
 
 참조 : https://joyhong.tistory.com/128
 
```

5. mecab 오류 발생 시
참조 : https://www.microsoft.com/ko-kr/download/details.aspx?id=48145


