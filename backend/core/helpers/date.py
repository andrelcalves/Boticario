from datetime import datetime

import pytz

from backend.core.config import settings


def now_datetime(timezone: str = settings.DEFAULT_TIMEZONE) -> datetime:
    return datetime.now(tz=pytz.timezone(timezone))
