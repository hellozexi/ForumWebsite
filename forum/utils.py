from uuid import uuid4
from datetime import datetime
from dateutil import parser


def new_uuid() -> str:
    return str(uuid4()).replace('-', '')


def check_datetime(d: str) -> bool:
    date = None
    try:
        date = parser.parse(d)
    except ValueError:
        return False
    finally:
        if date is None:
            return False
        return type(date) is datetime
