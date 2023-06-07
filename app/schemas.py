from datetime import datetime, date
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserBase(BaseModel):
    username: str
    first_name: str | None = None
    last_name: str | None = None
    birth: date | None = None
    email: str
    phone_number: str
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
    is_active: bool
    created_at: datetime
    updated_at: datetime 

    # TODO: tweets: List[Tweets]
    # TODO: comments: List[Comments]

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
    
