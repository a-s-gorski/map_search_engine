import logging
import os

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI

from app.api.endpoints.find_route import router as find_route_router
from app.repository.planet_osm_point_repository import (get_longitude_latitude,
                                                        get_osm_id)
from app.repository.ways_repository import (get_n_closest_gids,
                                            get_shortest_path,
                                            search_shortest_path)
from app.startup import start_up

app = FastAPI()


app.include_router(find_route_router)
