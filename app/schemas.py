from datetime import datetime, date
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
