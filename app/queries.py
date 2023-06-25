from sqlalchemy.orm import Session
from .models import Users


class Queries:
    @staticmethod
    def get_user(db: Session, username: str) -> Users | None:
        return db.query(Users).filter(Users.username == username).first()
