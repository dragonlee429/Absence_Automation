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
TIMEZONE_OFFSET = "+0100"

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


def get_today_absence():
    """오늘 휴가 여부 가져오기"""
    today = datetime.datetime.now(tz).date().isoformat()

    data = {
        "skip": 0,
        "limit": 1,
        "filter": {
            "start": {"$lte": today},
            "end": {"$gte": today},
            "assignedToId": API_KEY
        },
        "relations": ["assignedToId", "reasonId", "approverId"]
    }

    url = f"{BASE_URL}/absences"
    headers = get_hawk_auth(url, "POST", json.dumps(data))

    response = requests.post(url, headers=headers, json=data, verify=False)

    if response.status_code == 200:
        absences = response.json().get("data", [])
        if absences:
            print(f"휴가 감지됨: {absences}")
            return 200  # 휴가 있음
        else:
            print("오늘은 휴가가 아님")
            return None  # 휴가 없음
    else:
        print(f"[ERROR] 휴가 조회 실패: {response.status_code} - {response.text}")
        return None  # 요청 실패 시 None 반환


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

def create_new_timespan():
    """새로운 출근 기록(timespan) 생성 (오늘 휴가가 없을 경우에만)"""

    # 7시 50분에서 59분 사이의 랜덤한 분을 생성
    random_minute = random.randint(50, 59)

    # 현재 시간에서 7시 50분부터 59분 사이의 랜덤 시간으로 설정 (타임존 반영)
    new_start_time = datetime.datetime.now(tz).replace(hour=7, minute=random_minute, second=0, microsecond=0)

    # UTC로 변환 후 ISO 8601 형식으로 변환하고, 밀리초 및 Z 추가
    new_start_time_utc = new_start_time.astimezone(pytz.utc)  # UTC로 변환
    new_start_time_str = new_start_time_utc.strftime('%Y-%m-%dT%H:%M:%S.000Z')  # ISO 8601 형식

    data = {
        "userId": API_KEY,
        "start": new_start_time_str,
        "timezoneName": TIMEZONE,
        "timezone": TIMEZONE_OFFSET,
        "type": "work"
    }

    url = f"{BASE_URL}/timespans/create"
    headers = get_hawk_auth(url, "POST", json.dumps(data))

    response = requests.post(url, headers=headers, json=data, verify=False)

    if response.status_code == 200:
        print(f"새로운 출근 기록 생성 완료: {new_start_time_str}")
    else:
        print("새로운 출근 기록 생성 실패:", response.text)


def edit_start_time_random():
    """오늘 출근 시간을 7시 50분에서 59분 사이의 랜덤 시간으로 수정"""

    absence_status = get_today_absence()
    if absence_status == 200:
        print("오늘 휴가가 있어 출근 기록을 생성하지 않습니다.")
        return  # 아무 동작도 하지 않고 종료


    timespan_id = get_today_timespan()

    if not timespan_id:
        print("오늘 출근 기록이 없습니다. 새로운 출근 기록을 생성합니다.")
        create_new_timespan()
        return

    # 7시 50분에서 59분 사이의 랜덤한 분을 생성
    random_minute = random.randint(50, 59)

    # 현재 시간에서 7시 50분부터 59분 사이의 랜덤 시간으로 설정 (타임존 반영)
    new_start_time = datetime.datetime.now(tz).replace(hour=7, minute=random_minute, second=0, microsecond=0)

    # UTC로 변환 후 ISO 8601 형식으로 변환하고, 밀리초 및 Z 추가
    new_start_time_utc = new_start_time.astimezone(pytz.utc)  # UTC로 변환
    new_start_time_str = new_start_time_utc.strftime('%Y-%m-%dT%H:%M:%S.000Z')  # ISO 8601 형식

    data = {
        "start": new_start_time_str,
        "timezoneName": TIMEZONE,
        "timezone": TIMEZONE_OFFSET
    }

    url = f"{BASE_URL}/timespans/{timespan_id}"
    headers = get_hawk_auth(url, "PUT", json.dumps(data))

    response = requests.put(url, headers=headers, json=data, verify=False)

    if response.status_code == 200:
        print(f"출근 시간 {new_start_time_str}으로 수정 완료")
    else:
        print("출근 시간 수정 실패:", response.text)

if __name__ == "__main__":
    edit_start_time_random()
