from sqlalchemy.orm import Session

from app.api.models.planet_osm_point import PlanetOSMPoint
from app.api.models.ways import Ways

from .base import Base


def setup_db(db: Session) -> None:
    Base.metadata.create_all(bind=db.bind)
