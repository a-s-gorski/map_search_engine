from app.core.config import settings
from app.core.db import get_db
from app.db.base import Base
from app.db.setup import setup_db


def start_up():
    with get_db() as db:
        setup_db(db)
