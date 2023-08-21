from typing import Optional

from pydantic import BaseModel


class NavigationNode(BaseModel):
    name: Optional[str] = None
    length: float
    x1: float
    y1: float
    x2: float
    y2: float
    cost: float
