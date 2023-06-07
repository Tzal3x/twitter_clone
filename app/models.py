"""SQL Alchemy (ORM) & Alembic (Migration Tool)"""
from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy import (
    Column, ForeignKey, Unicode, UnicodeText, Integer, String, DateTime, Boolean,
    )
from app.database import Base


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(Unicode, nullable=False)
    first_name = Column(Unicode)
    last_name = Column(Unicode)
    birth = Column(DateTime)
    email = Column(String(254), nullable=False)
    phone_number = Column(String(15), nullable=False)
    bio = Column(Unicode(160))
    is_active = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    password = Column(String, nullable=False)

    tweets = relationship("Tweets", back_populates="user")
    comments = relationship("Comments", back_populates="user")


class Tweets(Base):
    __tablename__ = 'tweets'
    
    id = Column(Integer, primary_key=True)
    title = Column(Unicode, nullable=False)
    body = Column(UnicodeText, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    is_active = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    
    user = relationship("Users", back_populates="tweets")
    comments = relationship("Comments", back_populates="tweet")


class Comments(Base):
    __tablename__ = 'comments'
    
    id = Column(Integer, primary_key=True)
    body = Column(Unicode, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    tweet_id = Column(Integer, ForeignKey('tweets.id'))
    is_active = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    
    user = relationship("Users", back_populates="comments")
    tweet = relationship("Tweets", back_populates="comments")
    

""" Association tables """
class TweetLikes(Base):
    __tablename__ = 'tweet_likes'
    
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    tweet_id = Column(Integer, ForeignKey('tweets.id'), primary_key=True)
    is_active = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
     

class CommentLikes(Base):
    __tablename__ = 'comment_likes'
    
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    comment_id = Column(Integer, ForeignKey('comments.id'), primary_key=True)
    is_active = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)


class Follows(Base):
    # A follower follows the followee
    __tablename__ = 'follows'
    
    follower_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    followee_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    is_active = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
