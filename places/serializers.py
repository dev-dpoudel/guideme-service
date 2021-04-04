from typing import Optional, List
from pydantic import BaseModel
from mixin.baseOutput import BaseOut


# Class Declaration for Products
class PlaceBase(BaseModel):
    name: str
    category: Optional[str]
    country: Optional[str]
    city: Optional[str]
    location: Optional[List[str]]
    description: Optional[str]
    tags: Optional[str]


# Class Declaration for Input Serializers
class PlaceIn(PlaceBase):
    pass


# Class Declaration for Ouput Serializers
class PlaceOut(PlaceBase, BaseOut):
    pass
