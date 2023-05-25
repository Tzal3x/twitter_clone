"""SQL Alchemy (ORM) & Alembic (Migration Tool)"""
from datetime import datetime

from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey
    )


Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    birth = Column(DateTime)
    created = Column(DateTime, default=datetime.utcnow)
    tweets = relationship("Tweets", back_populates="user")
    comments = relationship("Comments", back_populates="user")


class Tweets(Base):
    __tablename__ = 'tweets'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("Users", back_populates="tweets")
    comments = relationship("Comments", back_populates="tweet")


class Comments(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    body = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'))
    tweet_id = Column(Integer, ForeignKey('tweets.id'))
    user = relationship("Users", back_populates="comments")
    tweet = relationship("Tweets", back_populates="comments")
    

""" Association tables """
class TweetLikes(Base):
    __tablename__ = 'tweet_likes'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    tweet_id = Column(Integer, ForeignKey('tweets.id'), primary_key=True)
     

class CommentLikes(Base):
    __tablename__ = 'comment_likes'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    comment_id = Column(Integer, ForeignKey('comments.id'), primary_key=True)


class Follows(Base):
    # A follower follows the followee
    __tablename__ = 'follows'
    follower_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    followee_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
