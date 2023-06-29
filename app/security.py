from typing import Annotated, Any
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import status, HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError
from app.models import Users
from app.helpers import get_security_configs
from app.queries import Queries
from app.database import get_db


security_configs = get_security_configs()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authenticate_user(db, username: str, password: str) -> Users | None:
    user = Queries.get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def authorize_user(token: Annotated[str, Depends(oauth2_scheme)],
                   db: Session = Depends(get_db)) -> Users:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        expiration_unix_timestamp = datetime.utcfromtimestamp(
            int(payload['exp'])
            )
        token_has_expired = datetime.utcnow() > expiration_unix_timestamp
        if token_has_expired:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = Queries.get_user(db, username=username)
    if user is None:
        raise credentials_exception

    return user


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict,
                        expires_delta: timedelta = timedelta(
                            minutes=security_configs["ACCESS_TOKEN_EXPIRE_MINUTES"]
                            )) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,
                             security_configs["TOKEN_CREATION_SECRET_KEY"],
                             algorithm=security_configs["HASH_ALGORITHM"])
    return encoded_jwt


def decode_access_token(token: str) -> dict[str, Any]:
    """
    Verify that the access token is valid.
    """

    return jwt.decode(token,
                      security_configs["TOKEN_CREATION_SECRET_KEY"],
                      algorithms=[security_configs["HASH_ALGORITHM"]])
