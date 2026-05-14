import calendar
import re
from datetime import date, timedelta


WORD_NUMS = {
    "a": 1,
    "an": 1,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
}


def _to_n(s: str) -> int | None:
    if s.isdigit():
        return int(s)
    return WORD_NUMS.get(s)


def parse(s: str, today: date | None = None) -> date:
    if today is None:
        today = date.today()

    s = s.strip().lower()

    if s in ("today", "now"):
        return today
    if s == "tomorrow":
        return today + timedelta(days=1)
    if s == "yesterday":
        return today + timedelta(days=-1)
    if s == "the day after tomorrow":
        return today + timedelta(days=2)
    if s == "the day before yesterday":
        return today + timedelta(days=-2)

    if s == "next week":
        return today + timedelta(weeks=1)
    if s == "last week":
        return today - timedelta(weeks=1)
    if s == "next month":
        return _add_months(today, 1)
    if s == "last month":
        return _add_months(today, -1)
    if s == "next year":
        return _add_months(today, 12)
    if s == "last year":
        return _add_months(today, -12)

    weekdays = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ]
    for i, day in enumerate(weekdays):
        if s == f"next {day}":
            days_ahead = (i - today.weekday() + 7) % 7 or 7
            return today + timedelta(days=days_ahead)
        if s in (f"last {day}", f"previous {day}"):
            days_ago = (today.weekday() - i + 7) % 7 or 7
            return today - timedelta(days=days_ago)
        if s in (f"this {day}", day):
            days_ahead = (i - today.weekday() + 7) % 7 or 7
            return today + timedelta(days=days_ahead)

    units = r"(day|days|week|weeks|month|months|year|years)"
    num = r"(\d+|[a-z]+)"

    m = re.fullmatch(rf"in {num} {units}", s)
    if m:
        n = _to_n(m.group(1))
        if n is not None:
            return _add_unit(today, n, m.group(2))

    m = re.fullmatch(rf"{num} {units} ago", s)
    if m:
        n = _to_n(m.group(1))
        if n is not None:
            return _add_unit(today, -n, m.group(2))

    m = re.fullmatch(rf"{num} {units} (before|after|from) (.+)", s)
    if m:
        n = _to_n(m.group(1))
        if n is not None:
            direction = 1 if m.group(3) in ("after", "from") else -1
            ref = parse(m.group(4), today)
            return _add_unit(ref, direction * n, m.group(2))

    # "2 years, 3 months before ..." or "2 years and 3 months before ..."
    m = re.fullmatch(
        rf"{num} years?(?:,| and|,? and) {num} months? (before|after|from) (.+)", s
    )
    if m:
        ny = _to_n(m.group(1))
        nm = _to_n(m.group(2))
        if ny is not None and nm is not None:
            direction = 1 if m.group(3) in ("after", "from") else -1
            ref = parse(m.group(4), today)
            return _add_months(ref, direction * (ny * 12 + nm))

    result = _parse_absolute(s)
    if result:
        return result

    raise ValueError(f"Cannot parse date: {s!r}")


def _add_unit(d: date, n: int, unit: str) -> date:
    if "day" in unit:
        return d + timedelta(days=n)
    if "week" in unit:
        return d + timedelta(weeks=n)
    if "month" in unit:
        return _add_months(d, n)
    if "year" in unit:
        return _add_months(d, n * 12)
    raise ValueError(f"Unknown unit: {unit}")


def _add_months(d: date, n: int) -> date:
    month = d.month - 1 + n
    year = d.year + month // 12
    month = month % 12 + 1
    day = min(d.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def _parse_absolute(s: str) -> date | None:
    months_map = {
        "january": 1,
        "february": 2,
        "march": 3,
        "april": 4,
        "may": 5,
        "june": 6,
        "july": 7,
        "august": 8,
        "september": 9,
        "october": 10,
        "november": 11,
        "december": 12,
        "jan": 1,
        "feb": 2,
        "mar": 3,
        "apr": 4,
        "jun": 6,
        "jul": 7,
        "aug": 8,
        "sep": 9,
        "oct": 10,
        "nov": 11,
        "dec": 12,
    }

    m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", s)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))

    m = re.fullmatch(r"(\d{4})/(\d{1,2})/(\d{1,2})", s)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))

    m = re.fullmatch(r"(\d{4})\.(\d{1,2})\.(\d{1,2})", s)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))

    m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", s)
    if m:
        return date(int(m.group(3)), int(m.group(1)), int(m.group(2)))

    m = re.fullmatch(r"(\d{1,2})-(\d{1,2})-(\d{4})", s)
    if m:
        return date(int(m.group(3)), int(m.group(1)), int(m.group(2)))

    m = re.fullmatch(r"([a-z]+\.?) (\d{1,2})(?:st|nd|rd|th)?,? (\d{4})", s)
    if m and m.group(1).rstrip(".") in months_map:
        return date(
            int(m.group(3)), months_map[m.group(1).rstrip(".")], int(m.group(2))
        )

    m = re.fullmatch(r"(\d{1,2})(?:st|nd|rd|th)? ([a-z]+\.?),? (\d{4})", s)
    if m and m.group(2).rstrip(".") in months_map:
        return date(
            int(m.group(3)), months_map[m.group(2).rstrip(".")], int(m.group(1))
        )

    return None
