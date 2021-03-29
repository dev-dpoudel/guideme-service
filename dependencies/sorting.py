# Provides Pagination Services as a Dependencies to API
from typing import Optional, List
from pydantic import BaseModel, Field
from fastapi import HTTPException, status


# Model for Sorting
class SortingModel(BaseModel):
    ''' Provides Model Definition for Filter '''
    field: str = Field(None, description="Sortby Filed Name", min_length=3)
    type: str = Field("asc", description="Sort type", min_length=3)


class Sorters:
    '''Sorting Class : Provides Ordering Support for Query Models'''

    _order_by = None
    _map = {"asc": "+", "desc": "-"}

    def __init__(self, sortinfo: Optional[List[SortingModel]]):

        if not sortinfo:
            return

        try:
            self._order_by = [self.get_expr(sort.field, sort.type) for sort in sortinfo]  # noqa E501
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid Orderby Parameters"
            )

    def get_expr(self, field: str, type: str):
        '''
        Set the filtering expression
        '''
        return "{}{}".format(self._map[type], field)

    def reset_sorter(self):
        ''' Reset the Filters declared previously '''
        self._order_by = None

    def get_order_by(self):
        ''' Get current active Sorters '''
        return self._order_by

    @staticmethod
    def get_mapping(cls):
        return cls._map

    @staticmethod
    def getDoc():
        return "Ordering"


# Filter Dependencies for Application
async def app_ordering(sortinfo: Optional[List[SortingModel]] = None):
    instance = Sorters(sortinfo)
    return instance.get_order_by()
