from fastapi import HTTPException, status
from passlib.context import CryptContext
from datetime import timedelta, datetime
from src.config import Config
import jwt
import uuid
import logging


password_context = CryptContext(
    schemes=['bcrypt']
)

ACCESS_TOKEN_EXPIRY = 3600

def generate_password_hash(password: str) -> str:
    hash = password_context.hash(password)
    return hash

def verify_password(password: str, hash: str) -> bool:
    return password_context.verify(password, hash)

def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool= False):
    payload = {}
    payload['user'] = user_data
    payload['exp'] = datetime.now() + (expiry if expiry is not None else timedelta(seconds=Config.ACCESS_TOKEN_EXPIRY))
    payload['jti'] = str(uuid.uuid4())
    
    payload['refresh'] = refresh
    
    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM
    )
    return token


def decode_token(token: str) -> dict:
    try :
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM]
        )
        return token_data
    except jwt.DecodeError as e:
        print(f"Decode error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token decode error: Invalid or corrupted token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Token error: {str(e)}")
