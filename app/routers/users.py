from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import app.schemas as schemas
from app.models import Users
from app.database import get_db
from app.security import get_password_hash, authorize_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, 
                db: Session = Depends(get_db),
                ) -> schemas.UserReturn:
    hashed_password = get_password_hash(user.password)
    user_body = user.dict()
    user_body["password"] = hashed_password
    db_user = Users(**user_body)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/me", status_code=status.HTTP_200_OK)
def get_user_info(user: Annotated[Users, Depends(authorize_user)]) -> schemas.UserReturn:
    # TODO add error handling and custom error messages
    if user:
        return user


@router.get("/{id}")
def get_user_info(id: int):
    pass  


@router.put("/")
def update_user_info():
    pass


@router.delete("/")
def delete_user_account():
    pass

