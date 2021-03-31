# Provides Pagination Services as a Dependencies to API
from typing import Optional
# from pydan import Field
from pydantic import BaseModel, Field


# Model for Pagination Class
class PageModel(BaseModel):
    ''' Provides Model Definition for Filter '''
    limit: int = Field(100, description="Max Rec Per Page", lt=1000, gte=1)
    skip: int = Field(0, description="Get Frome",  gte=0)


# Filter Dependencies for Application
async def pagination(limit: Optional[int] = 100, pageno: Optional[int] = 0):
    page = PageModel(limit=limit, skip=limit*pageno)
    return page
