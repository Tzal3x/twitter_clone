from typing import Annotated
from fastapi import APIRouter, Depends, Query, Body, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import exc
from app import schemas
from app.models import Users
from app.database import get_db
from app.security import get_password_hash, authorize_user
from app.queries import Queries


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserReturn)
def create_user(user: schemas.UserCreate, 
                db: Session = Depends(get_db),
                ) -> schemas.UserReturn:
    hashed_password = get_password_hash(user.password)
    user_body = user.dict()
    user_body["password"] = hashed_password
    db_user = Users(**user_body)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Username, email or phone number already exist.")
    return db_user


@router.get("/me", status_code=status.HTTP_200_OK)
def get_current(user: Annotated[Users, Depends(authorize_user)]) -> schemas.UserReturn:
    return user


@router.get("/", status_code=status.HTTP_200_OK)
def get_specific_user(username: Annotated[str, Query],
                      _: Annotated[Users, Depends(authorize_user)],
                      db: Session = Depends(get_db)) -> schemas.UserReturn:
    user = Queries.get_user(db, username)
    print(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found.")
    return user


# Using patch to partially update the user's info.
@router.patch("/", status_code=status.HTTP_204_NO_CONTENT)
def update_current_user_info(
    update_user: Annotated[schemas.UserUpdate, Body],
    user: Annotated[Users, Depends(authorize_user)],
    db: Session = Depends(get_db), 
    ):

    update_data = update_user.dict(exclude_unset=True)
    try:
        db.query(Users).filter(Users.username == user.username).update(update_data)
        db.commit()
    except exc.SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Could user not update fields.")  #TODO: Change status to a better suiting one


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_current_account(
    user: Annotated[Users, Depends(authorize_user)],
    db: Session = Depends(get_db), 
    ):
    try:
        db.query(Users).filter(Users.username == user.username).delete()
        db.commit()
    except exc.SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Could not delete user.") 
