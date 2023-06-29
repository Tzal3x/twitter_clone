from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

from .helpers import create_db_url

SQLALCHEMY_DATABASE_URL = create_db_url()
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

log = logging.getLogger(__name__)


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        log.exception(e)
    finally:
        db.close()
