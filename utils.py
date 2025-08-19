from typing import List
from datetime import date, datetime, timedelta

def today_iso_date() -> str:
    from datetime import datetime
    return datetime.today().strftime("%Y-%m-%d")


def now_iso_datetime() -> str:
    from datetime import datetime
    return datetime.now().isoformat(timespec='seconds')


def make_id(prefix: str = "hb") -> str:
    import random
    import string
    prepend = prefix + "_"
    return prepend + "".join(random.choices(string.ascii_lowercase, k=6))



# TODO: compute consecutive-day streak ending at today from history dates


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

# TODO: adherence in last n days (0..1)


def adherence(history: List[str], today: str, days: int = 30) -> float:
    today_date = date.fromisoformat(today)
    history_dates = set()
    counter = 0

    for d in history:
        converted = date.fromisoformat(d)
        if converted <= today_date:
            history_dates.add(converted)

    current = today_date

    for _ in range(days):
        if current in history_dates:
            counter += 1
            current -= timedelta(days=1)
    adherence = counter / days
    return adherence