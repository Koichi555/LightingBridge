from datetime import datetime
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Asia/Taipei")


def now_iso():
    return datetime.now(TZ).isoformat()
