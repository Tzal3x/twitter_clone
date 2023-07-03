from fastapi import APIRouter, status, HTTPException, Depends, Response
from app.models import TweetLikes, CommentLikes, Tweets, Comments
from app.schemas import UserReturn
from sqlalchemy.orm import Session
from sqlalchemy import exc
from app.database import get_db
from app.security import authorize_user
from typing import Annotated

router = APIRouter(
    prefix="/likes",
    tags=["likes"],
    responses={404: {"description": "Not found"}},
)


""" Likes on tweets """
@router.post('/tweet/{id}', status_code=status.HTTP_201_CREATED)
def add_like_to_tweet(id: int,
                      current_user: Annotated[UserReturn, Depends(authorize_user)],
                      db: Annotated[Session, Depends(get_db)]):

    '''
    We could optimize error handling here, by seperately check each case.
    However by letting the exception below handling both cases at once,
    we keep our code short and simple. Besides, there is no need for an extra
    query, which checks if tweet exists.
    '''
    like_on_tweet = TweetLikes(tweet_id=id, user_id=current_user.id)
    try:
        db.add(like_on_tweet)
        db.commit()
        db.refresh(like_on_tweet)
    except exc.SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"User with id: {current_user.id} has\
                                already liked tweet with id: {id}, or tweet\
                                    does not exist.")

    return Response(status_code=status.HTTP_201_CREATED)


@router.delete('/tweet/{id}', status_code=status.HTTP_204_NO_CONTENT)
def remove_like_from_tweet(id: int,
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

    like_on_tweet_query = db.query(TweetLikes).filter(TweetLikes.tweet_id == id, TweetLikes.user_id == current_user.id)

    like_on_tweet = like_on_tweet_query.first()

    if like_on_tweet is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {current_user.id} never liked this tweet in the first place")

    like_on_tweet_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# """ Likes on comments """
@router.post('/comment/{id}', status_code=status.HTTP_201_CREATED)
def add_like_to_comment(id: int,
                        current_user: Annotated[UserReturn, Depends(authorize_user)],
                        db: Annotated[Session, Depends(get_db)]):

    like_on_comment = CommentLikes(comment_id=id, user_id=current_user.id)
    try:
        db.add(like_on_comment)
        db.commit()
        db.refresh(like_on_comment)
    except exc.SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"User with id: {current_user.id} has\
                                already liked comment with id: {id},\
                                    or comment does not exist.")

    return Response(status_code=status.HTTP_201_CREATED)


@router.delete('/comment/{id}', status_code=status.HTTP_204_NO_CONTENT)
def remove_like_from_comment(id: int,
                             current_user: Annotated[UserReturn, Depends(authorize_user)],
                             db: Annotated[Session, Depends(get_db)]):

    comment_query = db.query(Comments).filter(Comments.id == id)

    comment = comment_query.first()

    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Comment with id: {id} does not exist")

    if comment.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    like_on_comment_query = db.query(CommentLikes).filter(CommentLikes.comment_id == id, CommentLikes.user_id == current_user.id)

    like_on_tweet = like_on_comment_query.first()

    if like_on_tweet is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {current_user.id} never liked this comment in the first place")

    like_on_comment_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
