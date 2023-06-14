"""
Endpoint regarding the followers/following mechanism.
"""
from typing import Annotated
from fastapi import APIRouter, status, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from sqlalchemy import exc

from app.database import get_db
from app.security import authorize_user
from app.models import Users, Follows
from app.queries import Queries
from app.schemas import FollowersReturn, FollowingReturn


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
            follower_id=user.id,
            followee_id=followee.id
        )
    try:
        db.add(new_follow_entry)
        db.commit()
    except exc.IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="User has already been followed.")


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def unfollow(username: Annotated[str, Query],
             user: Users = Depends(authorize_user),
             db: Session = Depends(get_db)):
    """Unfollow user"""
    followee: Users = Queries.get_user(db, username)
    rows_deleted: int = db.query(Follows)\
                          .filter(Follows.follower_id == int(user.id),
                                  Follows.followee_id == int(followee.id))\
                          .delete()
    if not rows_deleted:
        raise HTTPException(status_code=status.HTTP_410_GONE,
                            detail="Unfollowing was not possible.")
    db.commit()


@router.get("/followers", response_model=FollowersReturn)
def get_followers(username: Annotated[str, Query],
                  limit: int = 10,
                  _: Users = Depends(authorize_user),
                  db: Session = Depends(get_db)):  
    """Get the usernames of the followers of a user"""
    user: Users = Queries.get_user(db, username)
    query = db.query(Follows.follower_id, Users.username)\
              .filter(Follows.followee_id == user.id)\
              .join(Users, Users.id == Follows.follower_id)\
              .limit(limit)
    followers = query.all()
    usernames: list = (username for _, username in followers)

    return FollowersReturn(followers=usernames)


@router.get("/following", response_model=FollowingReturn)
def get_following(username: Annotated[str, Query],
                  limit: int = 10,
                  _: Users = Depends(authorize_user),
                  db: Session = Depends(get_db)):  
    """Get the usermames that a user follows"""
    user: Users = Queries.get_user(db, username)
    query = db.query(Follows.followee_id, Users.username)\
              .filter(Follows.follower_id == user.id)\
              .join(Users, Users.id == Follows.followee_id)\
              .limit(limit)
    followees = query.all()
    usernames: list = (username for _, username in followees)

    return FollowingReturn(followees=usernames)
