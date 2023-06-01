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

