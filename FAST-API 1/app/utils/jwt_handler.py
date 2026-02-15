from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "a-string-secret-at-least-256-bits-long"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 2



def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

       
