"""SQL Alchemy (ORM) & Alembic (Migration Tool)"""
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy import (
    Column, ForeignKey, Unicode,
    Integer, String, DateTime
    )
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy_utils import EmailType
from app.database import Base


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(Unicode(20), nullable=False, unique=True)
    password = Column(String, nullable=False)
    first_name = Column(Unicode(40))
    last_name = Column(Unicode(40))
    birth = Column(DateTime, nullable=False)
    email = Column(EmailType, nullable=False, unique=True)
    phone_number = Column(String(15), unique=True)
    bio = Column(Unicode(250))
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('NOW()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('NOW()'), nullable=False)

    tweets = relationship("Tweets", back_populates="user")
    comments = relationship("Comments", back_populates="user")
    mentions = relationship("MentionsOnTweets", back_populates="user")


class Tweets(Base):
    __tablename__ = 'tweets'

    id = Column(Integer, primary_key=True)
    title = Column(Unicode(250), nullable=False)
    body = Column(Unicode(10_000), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                     nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('NOW()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('NOW()'), nullable=False)

    user = relationship("Users", back_populates="tweets",
                        cascade="all, delete")
    comments = relationship("Comments", back_populates="tweet")
    hashtags = relationship("Hashtags", back_populates="tweet")
    mentions = relationship("MentionsOnTweets", back_populates="tweet")


class Comments(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    body = Column(Unicode(500), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                     nullable=False)
    tweet_id = Column(Integer, ForeignKey('tweets.id', ondelete='CASCADE'),
                      nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('NOW()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('NOW()'), nullable=False)

    user = relationship("Users", back_populates="comments",
                        cascade="all, delete")
    tweet = relationship("Tweets", back_populates="comments",
                         cascade="all, delete")


class Hashtags(Base):
    __tablename__ = 'hashtags'

    tweet_id = Column(Integer, ForeignKey('tweets.id', ondelete='CASCADE'),
                      nullable=False, primary_key=True)
    tags = Column(ARRAY(Unicode, dimensions=1))
    tweet = relationship("Tweets", back_populates="hashtags")


class MentionsOnTweets(Base):
    __tablename__ = 'mentions_on_tweets'

    tweet_id = Column(Integer, ForeignKey('tweets.id', ondelete='CASCADE'),
                      primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                     primary_key=True)
    tweet = relationship("Tweets", back_populates="mentions",
                         cascade="all, delete")
    user = relationship("Users", back_populates="mentions",
                        cascade="all, delete")


# region Association tables
class TweetLikes(Base):
    __tablename__ = 'tweet_likes'

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                     primary_key=True)
    tweet_id = Column(Integer, ForeignKey('tweets.id', ondelete='CASCADE'),
                      primary_key=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('NOW()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('NOW()'), nullable=False)


class CommentLikes(Base):
    __tablename__ = 'comment_likes'

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                     primary_key=True)
    comment_id = Column(Integer, ForeignKey('comments.id', ondelete='CASCADE'),
                        primary_key=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('NOW()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('NOW()'), nullable=False)


class Follows(Base):
    # A follower follows the followee
    __tablename__ = 'follows'

    follower_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                         primary_key=True)
    followee_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                         primary_key=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('NOW()'), nullable=False)
# endregion
