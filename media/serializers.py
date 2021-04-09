from typing import Optional, Any
from pydantic import BaseModel
from mixin.baseOutput import BaseOut


# Class Declaration for Products
class MediaBase(BaseModel):
    filename: str
    content: Optional[str]
    thread: Optional[Any]
    context: str
    user: Optional[Any]


class MediaIn(MediaBase):
    pass


class MediaOut(MediaBase, BaseOut):
    pass
