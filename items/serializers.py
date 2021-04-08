from typing import Optional, List, Any
from datetime import datetime
from pydantic import BaseModel
from mixin.baseOutput import BaseOut


# Class Declaration for Products
class ProductBase(BaseModel):
    name: str
    identity: Optional[str]
    category: Optional[str]
    description: Optional[str]
    price: Optional[float]
    available: Optional[bool]
    manufacture_date: Optional[datetime]
    expiry_date: Optional[datetime]
    tags: Optional[List[str]]


# Class Declaration for Input Serializers
class ProductIn(ProductBase):
    user: Optional[str]


# Class Declaration for Ouput Serializers
class ProductOut(ProductBase, BaseOut):
    owner: Optional[Any]


class ProductUpdate(ProductBase, BaseOut):
    name: Optional[str]
