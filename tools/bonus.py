# tools/bonus.py

from datetime import datetime, timedelta


def calculate(prev_log_date, today_logs_count):
    bonus = 0

    if prev_log_date:
        if prev_log_date.date() == (datetime.utcnow() - timedelta(days=1)).date():
            bonus += 3

    if today_logs_count >= 2:
        bonus += 5

    return bonus