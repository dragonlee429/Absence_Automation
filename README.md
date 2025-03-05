**# Absense API 생성 방법**
* https://app.absence.io/ 로그인
* 우측 상단 프로필 - Show Profile - Integration
* Generate API Key

**# 자동화 방법**
* 파이썬 가상환경에서 requests, pytz, mohawk 등 라이브러리 설치
* pip install pyinstaller 로 pyinstaller 인스톨
* .py 파일을 가상환경에 불러온 뒤 생성한 API ID 와 Key 값을 입력
* pyinstaller --onefile Create_Timespan.py / pyinstaller --onefile Close_Timespan.py 로 실행파일로 변환
* Task Scheduler 에서 자동화 설정

* 
