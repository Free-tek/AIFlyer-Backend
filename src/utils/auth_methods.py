import base64
from datetime import datetime, timedelta
import secrets
import string
import jwt
from .constants import HS256
import hashlib
import random
from src.utils.cypher import OBACipher
from src.core.config import settings
import pytz

def generate_secure_otp(length=6):
    digits = string.digits
    otp = "".join(secrets.choice(digits) for _ in range(length))
    return int(otp)



def get_current_date_in_timezone(timezone_str):
    user_tz = pytz.timezone(timezone_str)
    return datetime.now(user_tz)

def get_week_of_month(date_obj):
    first_day = date_obj.replace(day=1)
    adjusted_dom = date_obj.day + first_day.weekday()
    return (adjusted_dom - 1) // 7 + 1


def get_timestamp_after_minutes_from_now(mins: int):
    now = datetime.now()
    return int(
        (
            datetime(
                year=now.year,
                month=now.month,
                day=now.day,
                hour=now.hour,
                minute=now.minute,
                second=now.second,
            )
            + timedelta(minutes=mins)
        ).timestamp()
    )


def base64_encode_string(value: str):
    return base64.b64encode(value.encode("ascii")).decode("ascii")


def get_current_timestamp():

    return int(datetime.timestamp(datetime.now()))


def create_access_token(data: dict, expiry_in_mins: str, secret_key: str):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=expiry_in_mins)

    to_encode.update({"exp": expire, **data})

    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=HS256)

    return encoded_jwt


def verify_access_token(token: str, secret_key: str):

    try:
        payload = jwt.decode(token, secret_key, algorithms=[HS256])
        if not payload:
            return None
    except:
        return None

    return payload


def generate_md5_hash(password: str):
    return hashlib.md5(password.encode()).hexdigest()

def generate_id(length=20):
    characters = string.ascii_letters + string.digits + '-_'
    return ''.join(random.choice(characters) for _ in range(length))

def get_current_timestamp():
    
    return int(datetime.timestamp(datetime.now()))


def generate_entity_key_pair(
        encrptyion_secret_key
    ):
        cipher = OBACipher(encrptyion_secret_key=encrptyion_secret_key)

        return cipher.generate_keys()