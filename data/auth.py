from datetime import timedelta, datetime
from jose import jwt
from data.config import load_config


config = load_config(".env")


SECRET_KEY = config.token.secret_key
ALGORITHM = config.token.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = config.token.expire_minutes


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt