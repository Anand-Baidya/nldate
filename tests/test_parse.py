from datetime import date
from nldate.parse import parse


def test_today():
    today = date(2025, 6, 1)
    assert parse("today", today) == date(2025, 6, 1)


def test_tomorrow():
    today = date(2025, 6, 1)
    assert parse("tomorrow", today) == date(2025, 6, 2)


def test_yesterday():
    today = date(2025, 6, 1)
    assert parse("yesterday", today) == date(2025, 5, 31)


def test_in_n_days():
    today = date(2025, 6, 1)
    assert parse("in 5 days", today) == date(2025, 6, 6)


def test_n_days_ago():
    today = date(2025, 6, 1)
    assert parse("3 days ago", today) == date(2025, 5, 29)


def test_in_n_weeks():
    today = date(2025, 6, 1)
    assert parse("in 2 weeks", today) == date(2025, 6, 15)


def test_next_weekday():
    today = date(2025, 6, 1)  # Sunday
    assert parse("next monday", today) == date(2025, 6, 2)


def test_last_weekday():
    today = date(2025, 6, 4)  # Wednesday
    assert parse("last monday", today) == date(2025, 6, 2)


def test_n_days_before_absolute():
    today = date(2025, 6, 1)
    assert parse("5 days before december 1st, 2025", today) == date(2025, 11, 26)


def test_n_days_after_absolute():
    today = date(2025, 6, 1)
    assert parse("5 days after december 1st, 2025", today) == date(2025, 12, 6)


def test_years_and_months_after():
    today = date(2025, 6, 1)
    assert parse("1 year and 2 months after yesterday", today) == date(2026, 7, 31)


def test_absolute_iso():
    assert parse("2025-12-01") == date(2025, 12, 1)


def test_absolute_month_name():
    assert parse("december 1st, 2025") == date(2025, 12, 1)


def test_two_weeks_from_tomorrow():
    today = date(2025, 6, 1)
    assert parse("two weeks from tomorrow", today) == date(2025, 6, 16)


def test_in_n_months():
    today = date(2025, 6, 1)
    assert parse("in 3 months", today) == date(2025, 9, 1)