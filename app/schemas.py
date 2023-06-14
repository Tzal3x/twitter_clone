import re
from datetime import datetime, date
from pydantic import BaseModel, EmailStr, validator


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserBase(BaseModel):
    # Required
    username: str
    email: EmailStr
    phone_number: str

    # Optional
    first_name: str | None = None
    last_name: str | None = None
    birth: date | None = None
    bio: str | None = None


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    birth: date | None = None
    bio: str | None = None


class UserCreate(UserBase):
    password: str

    @validator('password')
    def is_strong(cls, password: str):
        """
        Verify the strength of 'password'
        """
        min_password_len = 8
        length_error = (
            len(password) < min_password_len,
            f"Needs at least {min_password_len} characters! "
            f"Current: {len(password)}."
            )
        digit_error = (re.search(r"\d", password) is None,
                       "Use at least 1 digit.")

        uppercase_error = (re.search(r"[A-Z]", password) is None,
                           "Use at least 1 uppercase letter.")

        lowercase_error = (re.search(r"[a-z]", password) is None,
                           "Use at least 1 lowercase letter.")

        regex = r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]'
        symbol_error = (re.search(regex, password) is None,
                        "Use at least 1 symbol.")

        errors = (length_error, digit_error,
                  uppercase_error, lowercase_error,
                  symbol_error)
        for error in errors:
            if error[0]:
                raise ValueError(f"Password is not strong enough: {error[1]}")
        return password


class UserReturn(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class FollowersReturn(BaseModel):
    followers: list[str] | list[None]


class FollowingReturn(BaseModel):
    followees: list[str] | list[None]


class TweetBase(BaseModel):
    title: str
    body: str


class TweetReturn(TweetBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class TweetUpdate(BaseModel):
    title: str | None = None
    body: str | None = None


class CommentCreate(BaseModel):
    body: str


class CommentReturn(CommentCreate):
    id: int
    user_id: int
    tweet_id: int
    created_at: datetime
    updated_at: datetime
