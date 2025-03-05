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
  
**#주의사항**
* _Create_Timespan.py 는 매일 아침 7시 50-59분 사이에서 랜덤으로 출근 시각을 기입합니다_
* _Close_Timespan.py 는 매일 저녁 5시 00-15분 사이에서 랜덤으로 퇴근 시각을 기입합니다_
* _Absence 시스템의 특성 상 기입하려는 출근/퇴근 시간이 현재 시간보다 나중의 시간이면 기입을 허용하지 않습니다. Task Scheduler 에서 자동화 설정 시 주의를 필요합니다. (예 : 현재시간 17:00, 퇴근 시간을 17:30 분으로 기입하려고 할 때 기입 불가)_
