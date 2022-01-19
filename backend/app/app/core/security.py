from datetime import datetime, timedelta
from typing import Any, Union
import secrets
from jose import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Security
from app.core.config import settings, API_KEY
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from app.core.messages import AUTH_REQ, NO_API_KEY
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

api_key = APIKeyHeader(name="token", auto_error=False)


ALGORITHM = "HS256"


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def validate_request(header: Optional[str] = Security(api_key)) -> bool:
    if header is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=NO_API_KEY, headers={}
        )
    if not secrets.compare_digest(header, str(API_KEY)):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail=AUTH_REQ, headers={}
        )
    return True