from typing import Optional, Any  # noqa
from pydantic import BaseModel, Field  # noqa
from bson import ObjectId


class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, ObjectId):
            raise ValueError("Not a valid ObjectId")
        return str(v)


class BaseOut(BaseModel):
    ''' Output model to cast ObjectId field'''
    id: Optional[ObjectIdStr] = Field(None,
                                      description="Unique ObjectId",
                                      alias="id")
