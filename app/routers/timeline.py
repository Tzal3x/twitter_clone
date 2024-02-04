from fastapi import APIRouter, Depends, status
from typing import Annotated, List
from app.models import Users, Follows, Tweets
from app.security import authorize_user
from app.database import get_db
from sqlalchemy.orm import Session
from app.schemas import TweetReturn
from sqlalchemy import desc

router = APIRouter(
    prefix="/timeline",
    tags=["timeline"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", status_code=status.HTTP_200_OK,
            response_model=List[TweetReturn])
def get_user_timeline(
        user: Annotated[Users, Depends(authorize_user)],
        db: Session = Depends(get_db),
        offset: int = 0,
        limit: int = 20):

    # TODO: add indexes for this join between Tweets and Follows
    query = db.query(Tweets)\
              .filter(Follows.follower_id == user.id)\
              .join(Follows, Tweets.user_id == Follows.followee_id)\
              .order_by(desc(Tweets.created_at))\
              .offset(offset)\
              .limit(limit)

    tweets_of_timeline = query.all()

    return tweets_of_timeline
