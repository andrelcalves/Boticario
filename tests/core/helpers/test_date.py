from datetime import datetime

from backend.core.helpers.date import now_datetime


def test_now_datetime_success():
    # Create
    now = now_datetime()

    # Assert
    assert isinstance(now, datetime)
