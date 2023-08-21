from typing import Optional

from pydantic import BaseModel


class SearchQuery(BaseModel):
    origin_city: str
    origin_street: Optional[str] = None
    origin_house_number: Optional[str] = None
    destination_city: str
    destination_street: Optional[str] = None
    destination_house_number: Optional[str] = None
    max_velocity: int
