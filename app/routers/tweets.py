from typing import Annotated, List
from fastapi import APIRouter, status, Response, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError
from app.database import get_db
from app.models import Tweets, Users
from app.schemas import TweetBase, TweetReturn, TweetUpdate, UserReturn
from app.security import authorize_user

router = APIRouter(
    prefix="/tweets",
    tags=["tweets"],
    responses={404: {"description": "Not found"}},
)

'''
TODO - Get user timeline (after implementing follows)
'''

@router.get('/per_user/me', response_model=List[TweetReturn])
def get_tweet(current_user: Annotated[UserReturn, Depends(authorize_user)], 
              db: Annotated[Session, Depends(get_db)]) -> List[TweetReturn]:
    
    tweets = db.query(Tweets).filter(current_user.id == Tweets.user_id).all()
    return tweets


@router.get('/per_user/{id}', response_model=List[TweetReturn])
def get_tweet(id: int,
              _: Annotated[UserReturn, Depends(authorize_user)],
              db: Annotated[Session, Depends(get_db)]) -> List[TweetReturn]:
    
    user = db.query(Users).filter(Users.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} was not found")
    
    tweets = db.query(Tweets).filter(id == Tweets.user_id).all()
    return tweets


@router.get('/{id}', response_model=TweetReturn)
def get_tweet(id: int, 
              _: Annotated[UserReturn, Depends(authorize_user)], 
              db: Annotated[Session, Depends(get_db)]) -> TweetReturn:
    
    tweet = db.query(Tweets).filter(Tweets.id == id).first()
    
    if not tweet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Tweet with id: {id} was not found")

    return tweet


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=TweetReturn)
def create_tweet(tweet: TweetBase, 
                 current_user: Annotated[UserReturn, Depends(authorize_user)], 
                 db: Annotated[Session, Depends(get_db)]) -> TweetReturn:
    new_tweet = Tweets(user_id = current_user.id, **tweet.dict())
    try:
        db.add(new_tweet)
        db.commit()
        db.refresh(new_tweet)
    except DataError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Title or body character limit exceeded")
        
    return new_tweet


@router.put('/{id}', response_model=TweetReturn)
def update_tweet(id: int, 
                 updated_tweet: Annotated[TweetUpdate, Body],
                 current_user: Annotated[UserReturn, Depends(authorize_user)], 
                 db: Annotated[Session, Depends(get_db)]) -> TweetReturn:
    
    tweet_query = db.query(Tweets).filter(Tweets.id == id)
    tweet = tweet_query.first()

    if tweet == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Tweet with id: {id} does not exist")

    if tweet.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    tweet_query.update(updated_tweet.dict(), synchronize_session=False)
    db.commit()
    return tweet_query.first()



@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_tweet(id: int, 
                 current_user: Annotated[UserReturn, Depends(authorize_user)], 
                 db: Annotated[Session, Depends(get_db)]):
    
    tweet_query = db.query(Tweets).filter(Tweets.id == id)

    tweet = tweet_query.first()

    if tweet == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Tweet with id: {id} does not exist")

    if tweet.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    tweet_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
