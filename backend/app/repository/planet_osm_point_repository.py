from typing import Optional, Tuple

from geoalchemy2.functions import ST_X, ST_Y, ST_Transform
from sqlalchemy.orm import Session

from app.api.models.planet_osm_point import PlanetOSMPoint


def get_osm_id(
        db: Session,
        city: str,
        street: Optional[str] = None,
        house_number: Optional[int] = None) -> Optional[int]:

    query = db.query(PlanetOSMPoint.osm_id).filter(
        PlanetOSMPoint.addr_city == city)

    if street:
        query = query.filter(PlanetOSMPoint.addr_street == street)

    if house_number:
        query = query.filter(PlanetOSMPoint.addr_housenumber == house_number)

    osm_id = query.first()

    if osm_id:
        return osm_id[0]

    if street:
        osm_id = db.query(
            PlanetOSMPoint.osm_id).filter(
            PlanetOSMPoint.addr_city == city,
            PlanetOSMPoint.addr_street == street).first()
        if osm_id:
            return osm_id[0]

    osm_id = db.query(PlanetOSMPoint.osm_id).filter(
        PlanetOSMPoint.addr_city == city).first()

    if osm_id:
        return osm_id[0]

    return None


def get_longitude_latitude(
        db: Session, osm_id: int) -> Optional[Tuple[float, float]]:
    query = db.query(
        ST_X(ST_Transform(PlanetOSMPoint.geom, 4326)).label('long'),
        ST_Y(ST_Transform(PlanetOSMPoint.geom, 4326)).label('lat')
    ).filter(PlanetOSMPoint.osm_id == osm_id)
    result = query.first()

    if result:
        return result[0], result[1]
    return None
