from typing import List, Optional, Any  # noqa
from pydantic import BaseModel, Field  # noqa
from mixin.baseOutput import BaseOut
from datetime import datetime


class Ratings(BaseModel):
    ''' Base Model to provide common field'''
    rating: Optional[float]
    review: str


class RatingsIn(Ratings):
    ''' Provides Ouput Schema for Ratings'''
    thread: str


class RatingsOut(Ratings, BaseOut):
    ''' Provides Ouput Schema for Ratings'''
    user: str


class Comments(BaseModel):
    ''' Base Model to provide common field'''
    comment: str


class CommentsIn(Comments):
    ''' Provides Ouput Schema for Ratings'''
    thread: str


class CommentsOut(Comments, BaseOut):
    ''' Base Model to provide Output schema for  Comments'''
    user: str
    modified_date: datetime = Field(None,
                                    description="Modified Date",
                                    )
