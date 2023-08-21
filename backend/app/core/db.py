from contextlib import contextmanager

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

Session = sessionmaker()


def get_engine() -> Engine:
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    return engine


@contextmanager
def get_db() -> Session:
    engine = get_engine()
    Session.configure(bind=engine, autocommit=False)
    session = Session()
    try:
        yield session
        session.commit()
    except BaseException:
        session.rollback()
        raise
    finally:
        session.close()
