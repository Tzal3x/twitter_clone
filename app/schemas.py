from datetime import datetime, date
from pydantic import BaseModel, EmailStr


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
