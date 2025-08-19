from typing import List
from datetime import date, datetime, timedelta

def today_iso_date() -> str:
    return datetime.today().strftime("%Y-%m-%d")


def now_iso_datetime() -> str:
    return datetime.now().isoformat(timespec='seconds')


def make_id(prefix: str = "hb") -> str:
    import random
    import string
    prepend = prefix + "_"
    return prepend + "".join(random.choices(string.ascii_lowercase, k=6))

def compute_streak(history: List[str], today: str) -> int:
    today_date = date.fromisoformat(today)

    history_dates = set()

    for d in history:
        converted = date.fromisoformat(d)
        if converted <= today_date:
            history_dates.add(converted)

    streak = 0
    current = today_date
    while current in history_dates:
        streak += 1
        current -= timedelta(days=1)
    return streak

def adherence(history: List[str], today: str, days: int = 30) -> float:
    today_date = date.fromisoformat(today)
    history_dates = set()
    counter = 0

    for d in history:
        converted = date.fromisoformat(d)
        if converted <= today_date:
            history_dates.add(converted)

    current = today_date

    if days <= 0:
        return 0.0
    
    for _ in range(days):
        if current in history_dates:
            counter += 1
        current -= timedelta(days=1)
    return counter / days