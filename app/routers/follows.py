"""
Endpoint regarding the following mechanism of twitter.
"""
from typing import Annotated
from fastapi import APIRouter, Query, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import exc

from app.database import get_db
from app.security import authorize_user
from app.models import Users, Follows
from app.queries import Queries


router = APIRouter(
    prefix="/follows",
    tags=["follows"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def follow(username: Annotated[str, Query],
           user: Users = Depends(authorize_user),
           db: Session = Depends(get_db)):
    """Command to follow a user"""
    followee: Users = Queries.get_user(db, username)
    new_follow_entry = Follows(
            follower_id = user.id,
            followee_id = followee.id
        )
    try:
        db.add(new_follow_entry)
        db.commit()
    except exc.IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="User has been already followed.")


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def unfollow(username: Annotated[str, Query],
             user: Users = Depends(authorize_user),
             db: Session = Depends(get_db)):
    """Unfollow user"""
    followee: Users = Queries.get_user(db, username)
    try:
        db.query(Follows).filter(Follows.follower_id == user.id,
                                 Follows.followee_id == followee.id).delete()
        db.commit()
    except exc.NoResultFound:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Not following.")


# @router.get("/followers")
# def get_followers(username: Annotated[str, Query]):
#     """Get a collection of the followers of a user"""
#     pass


# @router.get("/following")
# def get_following(username: Annotated[str, Query]):
#     """Get a collection of the users following a user"""
#     pass
