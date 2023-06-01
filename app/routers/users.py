from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import app.schemas as schemas
from app.models import Users
from app.database import get_db
from app.security import get_password_hash

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
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


@router.get("/me")
def get_user_info():
    pass  


@router.get("/{id}")
def get_user_info(id: int):
    pass  


@router.put("/")
def update_user_info():
    pass


@router.delete("/")
def delete_user_account():
    pass

