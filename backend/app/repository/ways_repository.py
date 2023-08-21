from sqlalchemy import cast, text
from typing import List
import json
from typing import List, Optional, Tuple, Union

from geoalchemy2.functions import ST_Distance
from sqlalchemy import ARRAY, Integer, case, cast, func, select, text
from sqlalchemy.orm import Session
from sqlalchemy.sql import func, text

from app.api.models.ways import Ways


def get_n_closest_gids(db: Session,
                       longitude: float,
                       latitude: float,
                       n: Optional[int] = 10) -> Optional[List[int]]:

    # as ST_MakePoint and ST_SETSRID are not implemented in geoalchemy I have
    # to pass the string to db directly
    point = f"SRID=4326;POINT({longitude} {latitude})"
    query = db.query(
        Ways.gid).order_by(
        func.pow(
            Ways.x1 -
            longitude,
            2) +
        func.pow(
            Ways.y1 -
            latitude,
            2)).limit(n)
    result = query.all()
    if result:
        result = [gid[0] for gid in result]
    return result


def search_shortest_path(db: Session,
                         origin_gids: List[int],
                         destination_gids: List[int],
                         max_velocity: Optional[int] = 250) -> Optional[Tuple[int,
                                                                              int,
                                                                              float]]:
    """
    """
    subquery = f'SELECT gid as id, source, target, length / LEAST( maxspeed_forward, {max_velocity} ) AS cost  FROM ways',
    query = text("SELECT start_vid, end_vid, sum(cost) as total_cost FROM pgr_dijkstra(:sql, :origins, :destinations, directed => true) AS path GROUP BY start_vid, end_vid ORDER BY total_cost ASC LIMIT 1")
    query = query.bindparams(
        sql=subquery,
        origins=origin_gids,
        destinations=destination_gids,
    )
    result = db.execute(query).fetchall()

    if not result:
        return None
    optimal_start_vid, optimal_end_vid, cost = result[0]

    return optimal_start_vid, optimal_end_vid, cost


def get_shortest_path(db: Session,
                      orgin_gid: int,
                      destination_gid: int,
                      max_velocity: Optional[int] = 250) -> List[Tuple[Optional[str],
                                                                       float,
                                                                       float,
                                                                       float,
                                                                       float,
                                                                       float,
                                                                       float]]:
    source = db.query(Ways.source).filter(Ways.gid == orgin_gid).limit(1).all()
    if not source:
        raise Exception("Could not find orgin_gid")
    source_id = source[0][0]
    destination = db.query(Ways.target).filter(
        Ways.gid == destination_gid).limit(1).all()
    if not destination:
        raise Exception("Could not find destination gid")
    destionation_id = destination[0][0]
    subquery = f'SELECT gid as id, source, target, length / LEAST ( {max_velocity} , maxspeed_forward ) as cost, length / LEAST ( {max_velocity} , maxspeed_backward) as reverse_cost, x1, y1, x2, y2  FROM ways ORDER BY id',
    query = text("SELECT * FROM pgr_astar(:sql, :origins, :destinations, directed => true, heuristic := 0) AS path JOIN ways ON path.edge = ways.gid")
    query = query.bindparams(
        sql=subquery,
        origins=source_id,
        destinations=destionation_id,
    )
    result = db.execute(query)
    result = result.fetchall()
    result = list(
        map(lambda x: [x[11], x[9], x[-8], x[-7], x[-6], x[-5], x[4]], result))
    return result


def get_optimal_path(db: Session,
                     start_lon: int,
                     start_lat: int,
                     end_lon: int,
                     end_lat: int,
                     max_velocity: Optional[int] = 250,
                     n: Optional[int] = 30) -> List[Tuple[Optional[str],
                                                          float,
                                                          float,
                                                          float,
                                                          float,
                                                          float,
                                                          float]]:
    start_gids = get_n_closest_gids(db, start_lon, start_lat, n)
    end_gids = get_n_closest_gids(db, end_lon, end_lat, n)
    optimal_start, optimal_end, _ = search_shortest_path(
        db, start_gids, end_gids, max_velocity)
    shortest_route = get_shortest_path(
        db, optimal_start, optimal_end, max_velocity)
    return shortest_route
