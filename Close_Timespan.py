import requests
import json
import datetime
import pytz
import random
from mohawk import Sender

# Absence API 정보
BASE_URL = "https://app.absence.io/api/v2"
API_KEY = "{Your API ID}"
API_SECRET = "{Your API Key}"
TIMEZONE = "Europe/Berlin"

# 현재 시간 (유럽 중앙 시간 설정)
tz = pytz.timezone("Europe/Berlin")

def get_hawk_auth(url, method, content=""):
    """Hawk 인증 헤더 생성"""
    sender = Sender(
        credentials={"id": API_KEY, "key": API_SECRET, "algorithm": "sha256"},
        url=url,
        method=method,
        content=content,
        content_type="application/json",
    )
    return {"Authorization": sender.request_header}

def get_today_timespan():
    """오늘 날짜의 출근 기록(timespan) 가져오기"""
    today = datetime.datetime.now(tz).date().isoformat()

    data = {
        "filter": {
            "userId": API_KEY,
            "start": {"$gte": today},
            "end": {"$eq": None}
        },
        "limit": 1,
        "skip": 0
    }

    url = f"{BASE_URL}/timespans"
    headers = get_hawk_auth(url, "POST", json.dumps(data))

    response = requests.post(url, headers=headers, json=data, verify=False)
    print(response.status_code)
    print(response.text)
    if response.status_code == 200:
        timespans = response.json().get("data", [])
        return timespans[0]["_id"] if timespans else None
    else:
        print("timespan 조회 실패:", response.text)
        return None

def edit_start_time_random():
    """오늘 퇴근 시간을 17시 00분에서 15분 사이의 랜덤 시간으로 수정"""

    timespan_id = get_today_timespan()

    # 17시 00분에서 15분 사이의 랜덤한 분을 생성
    random_minute = random.randint(00, 15)

    # 현재 시간에서 17시 00분부터 15분 사이의 랜덤 시간으로 설정 (타임존 반영)
    new_end_time = datetime.datetime.now(tz).replace(hour=17, minute=random_minute, second=0, microsecond=0)

    # UTC로 변환 후 ISO 8601 형식으로 변환하고, 밀리초 및 Z 추가
    new_end_time_utc = new_end_time.astimezone(pytz.utc)  # UTC로 변환
    new_end_time_str = new_end_time_utc.strftime('%Y-%m-%dT%H:%M:%S.000Z')  # ISO 8601 형식

    data = {
        "end": new_end_time_str,
        "timezoneName": TIMEZONE,
        "timezone": new_end_time.strftime('%z')
    }

    url = f"{BASE_URL}/timespans/{timespan_id}"
    headers = get_hawk_auth(url, "PUT", json.dumps(data))

    response = requests.put(url, headers=headers, json=data, verify=False)
    print(response.status_code)
    print(response.text)
    if response.status_code == 200:
        print(f"퇴근 시간 {new_end_time_str}으로 수정 완료")
    else:
        print("퇴근 시간 수정 실패:", response.text)


if __name__ == "__main__":
    edit_start_time_random()
