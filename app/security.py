from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from app.models import Users
from app.helpers import get_security_configs
from app.queries import Queries


security_configs = get_security_configs()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Authenticator:
    @staticmethod
    def authenticate_user(db, username: str, password: str) -> Users | None:
        user = Queries.get_user(db, username)
        if not user:
            return False
        if not Authenticator.verify_password(password, user.password):
            return False
        return user    

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        marinated_password = plain_password + security_configs["PASSWORD_HASH_SALT"]
        return pwd_context.verify(marinated_password, hashed_password)


def get_password_hash(password: str) -> str:
    marinated_password = password + security_configs["PASSWORD_HASH_SALT"]
    return pwd_context.hash(marinated_password)


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

