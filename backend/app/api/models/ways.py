from geoalchemy2 import Geometry
from sqlalchemy import Column, Float, Integer, String

from app.db.base import Base


class Ways(Base):
    __tablename__ = 'ways'

    gid = Column(Integer, primary_key=True)
    osm_id = Column(Integer)
    tag_id = Column(Integer)
    length = Column(Float)
    length_m = Column(Float)
    name = Column(String)
    source = Column(Integer)
    target = Column(Integer)
    source_osm = Column(Integer)
    target_osm = Column(Integer)
    cost = Column(Float)
    reverse_cost = Column(Float)
    cost_s = Column(Float)
    reverse_cost_s = Column(Float)
    rule = Column(String)
    one_way = Column(Integer)
    oneway = Column(String)
    x1 = Column(Float)
    y1 = Column(Float)
    x2 = Column(Float)
    y2 = Column(Float)
    maxspeed_forward = Column(Float)
    maxspeed_backward = Column(Float)
    priority = Column(Float, default=1)
    the_geom = Column(Geometry('LINESTRING', srid=4326))
