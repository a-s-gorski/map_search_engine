from typing import List

from fastapi import HTTPException

from app.api.schemas.navigation_node import NavigationNode
from app.api.schemas.search_query import SearchQuery
from app.core.db import get_db
from app.repository.planet_osm_point_repository import (get_longitude_latitude,
                                                        get_osm_id)
from app.repository.ways_repository import get_optimal_path

from . import router


@router.post("/find_route", response_model=List[NavigationNode])
async def read_example(search_query: SearchQuery) -> List[NavigationNode]:
    with get_db() as db:
        start_osm_id = get_osm_id(
            db,
            search_query.origin_city,
            search_query.origin_street,
            search_query.origin_house_number)

        if not start_osm_id:
            raise HTTPException(
                status_code=404, detail="Start location cannot be found")

        end_osm_id = get_osm_id(
            db,
            search_query.destination_city,
            search_query.destination_street,
            search_query.destination_house_number)
        if not end_osm_id:
            raise HTTPException(
                status_code=404, detail="End location cannot be found")

        start_lon, start_lat = get_longitude_latitude(db, start_osm_id)
        end_lon, end_lat = get_longitude_latitude(db, end_osm_id)
        shortest_route = get_optimal_path(
            db,
            start_lon,
            start_lat,
            end_lon,
            end_lat,
            search_query.max_velocity)

    if not shortest_route:
        raise HTTPException(status_code=404, detail="Could not estabilish")

    shortest_route_response = list(map(lambda node: NavigationNode(
        name=node[0],
        length=node[1],
        x1=node[2],
        y1=node[3],
        x2=node[4],
        y2=node[5],
        cost=node[6]
    ), shortest_route))
    return shortest_route_response
