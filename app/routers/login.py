from fastapi import APIRouter, Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.security import Authenticator, create_access_token
from app.database import get_db
from typing import Annotated
from app.schemas import Token


router = APIRouter(
    prefix="/token",
    tags=["login"]
    )


@router.post("/")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                db: Session = Depends(get_db)) -> Token:
    user = Authenticator.authenticate_user(db, form_data.username, form_data.password)
    if _authentication_failed := not user:
        raise HTTPException(status_code=400, 
                            detail="Incorrect username or password")
    return Token(access_token=create_access_token(data={'sub': user.username}))
