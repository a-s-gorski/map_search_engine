from geoalchemy2 import Geometry
from sqlalchemy import JSON, BigInteger, Column, String
from sqlalchemy.ext.declarative import declarative_base

from app.db.base import Base


class PlanetOSMPoint(Base):
    __tablename__ = 'planet_osm_point'

    osm_id = Column(BigInteger, primary_key=True)
    addr_housenumber = Column('addr:housenumber', String)
    addr_street = Column('addr:street', String)
    addr_city = Column('addr:city', String)
    tags = Column(JSON)
    geom = Column('way', Geometry('POINT', srid=3857))
