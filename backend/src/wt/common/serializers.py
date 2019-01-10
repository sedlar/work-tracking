from datetime import datetime
from typing import Optional

from dateutil import parser


def remove_nones(response: dict) -> dict:
    final_response = {}
    for key, value in response.items():
        if isinstance(value, dict):
            final_response[key] = remove_nones(value)
        elif value is not None:
            final_response[key] = value
    return final_response


def serialize_datetime(timestamp: Optional[datetime]) -> Optional[str]:
    if timestamp is not None:
        return timestamp.isoformat()
    return None


def deserialize_datetime(serialized_timestamp: Optional[str]) -> Optional[datetime]:
    if serialized_timestamp:
        return parser.parse(serialized_timestamp)
    return None
