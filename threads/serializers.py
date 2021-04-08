from typing import List, Optional, Any  # noqa
from pydantic import BaseModel, Field  # noqa
from mixin.baseOutput import BaseOut
from authentication.serializers import UserOut
from datetime import datetime


class Threads(BaseModel):
    ''' Base model for thread definition'''
    thread: Any


class Ratings(BaseModel):
    ''' Base Model to provide common field'''
    rating: float
    review: str


class RatingsIn(Ratings, Threads):
    ''' Provides Ouput Schema for Ratings'''
    user: Optional[str]


class RatingsOut(Ratings, BaseOut):
    ''' Provides Ouput Schema for Ratings'''
    owner: Optional[Any]


class RatingsUpdate(Ratings):
    ''' Provides Ouput Schema for Ratings'''
    review: Optional[str]


class Comments(BaseModel):
    ''' Base Model to provide common field'''
    comment: str


class CommentsIn(Comments, Threads):
    ''' Provides Ouput Schema for Ratings'''
    user: Optional[str]


class CommentsOut(Comments, BaseOut):
    ''' Base Model to provide Output schema for  Comments'''
    owner: Optional[Any]
    modified_date: datetime = Field(None,
                                    description="Modified Date",
                                    )


class CommentsUpdate(Comments):
    ''' Comments Update Serializers '''
    pass
