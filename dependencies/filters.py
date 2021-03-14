# Provides Pagination Services as a Dependencies to API
from typing import Optional, List
from fastapi import Form
from pydantic import BaseModel


# Model for Pagination Class
class FilerModel(BaseModel):
    ''' Provides Model Definition for Filter '''
    field: str = Form(..., description="Current Page Number", ge=1)
    value: str = Form(..., description="Records per page", ge=1, le=100)
    expr: str = Form(..., description="Expression type", min_length=2)


class Filter:
    '''Filter Class : Provides Filtering Support for Query Models'''

    def __init__(self, filterinfo: Optional[List[FilerModel]]):
        self.filters = filterinfo

    def reset_filter(self):
        ''' Reset the Filters declared previously '''
        self.filters = []

    @classmethod
    def get_filter_info(cls):
        return cls.filters

    @staticmethod
    def getDoc():
        return str(Filter)
