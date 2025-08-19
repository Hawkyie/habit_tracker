# Utility function signatures only (no implementations).


from typing import List
from datetime import date



def today_iso_date() -> str:
    from datetime import datetime
    return datetime.today().strftime("%Y-%m-%d")


def now_iso_datetime() -> str:
    from datetime import datetime
    return datetime.now().isoformat()


def make_id(prefix: str = "hb") -> str:
    import random
    import string
    prepend = prefix + "_"
    return prepend + "".join(random.choices(string.ascii_lowercase, k=6))



# TODO: compute consecutive-day streak ending at today from history dates


def compute_streak(history: List[str], today: str) -> int: ...


# TODO: adherence in last n days (0..1)


def adherence(history: List[str], today: str, days: int = 30) -> float: ...