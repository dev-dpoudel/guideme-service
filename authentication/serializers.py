from typing import Optional, List, Dict
from pydantic import BaseModel, Field


# Model for User Authentication
class User(BaseModel):
    name: str = Field(..., description="Name of the Items", max_length=50)
    description: Optional[str] = Field(None, description="Product Desc")
    price: float = Field(..., description="Price of Item per unit", gt=0)
    tax: Optional[float] = Field(None, description="Taxation Rate", lt=50)
    tags: List[str]

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }
