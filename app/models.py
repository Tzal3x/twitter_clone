"""SQL Alchemy (ORM) & Alembic (Migration Tool)"""
import re
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy import (
    Column, ForeignKey, Unicode,
    Integer, String, DateTime,
    )
from sqlalchemy_utils import EmailType
from app.database import Base
import phonenumbers


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(Unicode(20), nullable=False, unique=True)
    password = Column(String, nullable=False)
    first_name = Column(Unicode(40))
    last_name = Column(Unicode(40))
    birth = Column(DateTime, nullable=False)
    email = Column(EmailType, nullable=False, unique=True)
    phone_number = Column(String(15), nullable=False, unique=True)
    bio = Column(Unicode(250))
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('NOW()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('NOW()'), nullable=False)

    tweets = relationship("Tweets", back_populates="user")
    comments = relationship("Comments", back_populates="user")

    @validates('username')
    def validate_username(self, username):
        Validator.min_length(username, 4)

    @validates('password')
    def validate_password(self, password):
        Validator.min_length(password, 4)
        Validator.is_strong(password)

    @validates('phone_number')
    def validate_phone_number(self, phone_number):
        Validator.is_phone_number(phone_number)


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


class Validator:
    """
    Helper class that validates field constraints.
    """
    @staticmethod
    def min_length(column_field: str, length: int) -> str:
        """
        Checks if a string field
        """
        if len(column_field) < length:
            error_msg = (
                f"{column_field} is too short! "
                f"Must be at least >= {length}."
            )
            raise ValueError(error_msg)
        return column_field

    @staticmethod
    def is_strong(password: str):
        """
        Verify the strength of 'password'
        """
        length_error = len(password) < 8
        digit_error = re.search(r"\d", password) is None
        uppercase_error = re.search(r"[A-Z]", password) is None
        lowercase_error = re.search(r"[a-z]", password) is None
        regex = r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]'
        symbol_error = re.search(regex, password) is None
        password_ok = not (length_error or digit_error or
                           uppercase_error or lowercase_error or
                           symbol_error)
        if not password_ok:
            error_msg = (
                "Password is not strong enough!"
                "Please check the following:\n"
                "- 8 characters length or more\n"
                "- 1 digit or more\n"
                "- 1 symbol or more\n"
                "- 1 uppercase letter or more\n"
                "- 1 lowercase letter or more\n"
            )
            raise ValueError(error_msg)
        return password

    @staticmethod
    def is_phone_number(phone_number) -> str:
        pn = phonenumbers.parse(phone_number, None)
        if not phonenumbers.is_valid_number(pn):
            raise ValueError("Not a valid phone number.")
        return phone_number
