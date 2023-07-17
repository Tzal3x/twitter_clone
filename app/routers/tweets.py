from typing import Annotated, List
from fastapi import APIRouter, status, Response, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError
from sqlalchemy import desc
from app.database import get_db
from app.models import Tweets, Users, Hashtags, MentionsOnTweets
from app.schemas import TweetBase, TweetReturn, TweetUpdate, UserReturn
from app.security import authorize_user
from app.helpers import MetadataExtractor

router = APIRouter(
    prefix="/tweets",
    tags=["tweets"],
    responses={404: {"description": "Not found"}},
)


def get_mentions_from_mention_tags(tweet_id: int,
                                   mention_tags: list[str] | list[None],
                                   db: Session
                                   ) -> list[MentionsOnTweets]:
    mentions_for_db = []
    for tag in mention_tags:
        user = db.query(Users).filter(Users.username == tag).first()
        if user:
            mentions_for_db.append(
                MentionsOnTweets(tweet_id=tweet_id,
                                 user_id=user.id))
    return mentions_for_db


@router.get('/per_user/me', response_model=List[TweetReturn])
def get_current_users_tweets(
        current_user: Annotated[UserReturn, Depends(authorize_user)],
        db: Annotated[Session, Depends(get_db)],
        offset: int = 0,
        limit: int = 10) -> List[TweetReturn]:

    tweets = db.query(Tweets)\
               .filter(current_user.id == Tweets.user_id)\
               .order_by(desc(Tweets.created_at))\
               .offset(offset)\
               .limit(limit)\
               .all()
    return tweets


@router.get('/per_user/{id}', response_model=List[TweetReturn])
def get_tweets_per_user(id: int,
                        _: Annotated[UserReturn, Depends(authorize_user)],
                        db: Annotated[Session, Depends(get_db)],
                        offset: int = 0,
                        limit: int = 10) -> List[TweetReturn]:
    user = db.query(Users)\
             .filter(Users.id == id)\
             .first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} was not found")

    tweets = db.query(Tweets)\
               .filter(id == Tweets.user_id)\
               .order_by(desc(Tweets.created_at))\
               .offset(offset)\
               .limit(limit)\
               .all()
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


@router.post('/', status_code=status.HTTP_201_CREATED,
             response_model=TweetReturn)
def create_tweet(tweet: TweetBase,
                 current_user: Annotated[UserReturn, Depends(authorize_user)],
                 db: Annotated[Session, Depends(get_db)]) -> TweetReturn:
    new_tweet = Tweets(user_id=current_user.id, **tweet.dict())
    try:
        db.add(new_tweet)
        db.commit()
        db.refresh(new_tweet)
    except DataError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Title or body character limit exceeded")

    hashtags = MetadataExtractor.extract_hashtags(tweet.dict())
    if hashtags:
        hashtags_for_db = Hashtags(tweet_id=new_tweet.id, tags=hashtags)
        try:
            db.add(hashtags_for_db)
            db.commit()
        except DataError:
            pass  # Failed to create hashtags

    mention_tags = MetadataExtractor.extract_mentions(tweet.dict())
    if mention_tags:
        try:
            mentions_for_db = get_mentions_from_mention_tags(new_tweet.id,
                                                             mention_tags,
                                                             db)
            if mentions_for_db:
                db.add_all(mentions_for_db)
                db.commit()
        except DataError:
            pass  # Failed to create mentions
    return new_tweet


@router.put('/{id}', response_model=TweetReturn)
def update_tweet(id: int,
                 updated_tweet: Annotated[TweetUpdate, Body],
                 current_user: Annotated[UserReturn, Depends(authorize_user)],
                 db: Annotated[Session, Depends(get_db)]) -> TweetReturn:

    tweet_query = db.query(Tweets).filter(Tweets.id == id)
    tweet = tweet_query.first()
    if tweet is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Tweet with id: {id} does not exist")
    if tweet.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action")
    tweet_query.update(updated_tweet.dict(), synchronize_session=False)
    db.commit()

    hashtags = MetadataExtractor.extract_hashtags(updated_tweet.dict())
    hashtags_for_db = Hashtags(tweet_id=tweet.id, tags=hashtags)
    if not hashtags:
        hashtag_query = db.query(Hashtags).filter(Hashtags.tweet_id == id)
        hashtag_query.delete(synchronize_session=False)
        db.commit()
    elif tweet.hashtags:
        hashtag_query = db.query(Hashtags).filter(Hashtags.tweet_id == id)
        hashtag_query.update({"tags": hashtags})
        db.commit()
    else:
        db.add(hashtags_for_db)
        db.commit()

    mention_tags = MetadataExtractor.extract_mentions(updated_tweet.dict())
    mentions_updated = get_mentions_from_mention_tags(id,
                                                      mention_tags,
                                                      db)
    if not mentions_updated:
        mention_query = db.query(MentionsOnTweets)\
            .filter(MentionsOnTweets.tweet_id == id)
        mention_query.delete(synchronize_session=False)
        db.commit()
    elif tweet.mentions:
        try:
            old_mentions = [mention.user_id for mention in tweet.mentions]
            new_mentions = [mention.user_id for mention in mentions_updated]
            mentions_to_delete = list(set(old_mentions)
                                      .difference(new_mentions))
            mentions_to_add = list(set(new_mentions).difference(old_mentions))
            mentions_to_add = [MentionsOnTweets(tweet_id=id, user_id=user_id)
                               for user_id in mentions_to_add]
            if mentions_to_add:
                db.add_all(mentions_to_add)
                db.commit()
            if mentions_to_delete:
                for user_id in mentions_to_delete:
                    mention_query = db.query(MentionsOnTweets)\
                        .filter(MentionsOnTweets.tweet_id == id,
                                MentionsOnTweets.user_id == user_id)
                    mention_query.delete(synchronize_session=False)
                    db.commit()
        except DataError:
            pass  # Failed to update mentions
    else:
        db.add_all(mentions_updated)
        db.commit()

    return tweet_query.first()


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_tweet(id: int,
                 current_user: Annotated[UserReturn, Depends(authorize_user)],
                 db: Annotated[Session, Depends(get_db)]):

    tweet_query = db.query(Tweets).filter(Tweets.id == id)

    tweet = tweet_query.first()

    if tweet is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Tweet with id: {id} does not exist")

    if tweet.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action")

    tweet_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
