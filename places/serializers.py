from typing import Optional, List, Any
from pydantic import BaseModel
from mixin.baseOutput import BaseOut


# Class Declaration for Products
class PlaceBase(BaseModel):
    name: str
    category: Optional[str]
    country: str
    city: str
    location: Optional[List[str]]
    description: Optional[str]
    tags: Optional[List[str]]


# Class Declaration for Input Serializers
class PlaceIn(PlaceBase):
    user: Optional[str]


# Class Declaration for Ouput Serializers
class PlaceOut(PlaceBase, BaseOut):
    owner: Optional[Any]


# Class Declaration for Update Serializers
class PlaceUpdate(PlaceBase):
    name: Optional[str]
    country: Optional[str]
    city: Optional[str]
