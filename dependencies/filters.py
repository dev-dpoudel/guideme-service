# Provides Pagination Services as a Dependencies to API
from typing import Optional, List, Any
from fastapi import Form
from pydantic import BaseModel
from mongoengine.queryset.visitor import Q


# Model for Pagination Class
class FilterModel(BaseModel):
    ''' Provides Model Definition for Filter '''
    field: str = Form(None, description="Filtered Filed Name", min_length=3)
    value: Any = Form(None, description="Filter Value")
    expr: str = Form(None, description="Comparison type", min_length=2)
    combine: str = Form("and", description="Combination type", min_length=2)


class Filters:
    '''Filter Class : Provides Filtering Support for Query Models'''

    _filters = None
    _type = None

    def __init__(self, filterinfo: Optional[List[FilterModel]]):

        if not filterinfo:
            return

        self._filters = filterinfo
        self._type = None
        # Find the type of filters to be built
        for i in filterinfo:
            if i.combine == "or":
                self._type = "Query"
                break

        if self._type == "Query":
            self._set_query()

        else:
            self._set_filter()

    @staticmethod
    def get_expr(field: str, expr: str):
        '''
        Set the filtering expression
        '''
        # key = field if expr == "eq" else field + "__" + expr
        return field if expr == "eq" else "{}__{}".format(field, expr)

    def _set_filter(self):
        '''
         Set Filter Parameters.
         Output : dict
        '''
        filter = {self.get_expr(instance.field, instance.expr): instance.value
                  for instance in self._filters
                  }
        # Set Filters
        self._filters = filter

    def _set_query(self):
        '''
        Set Query Objects
        Output: Q object
        '''
        query: Q = Q()
        for q in self._filters:
            if q.combine == "or":
                query |= Q(**{self.get_expr(q.field, q.expr): q.value})
            else:
                query &= Q(**{self.get_expr(q.field, q.expr): q.value})

        # Set Filters
        self._filters = query

    def reset_filter(self):
        ''' Reset the Filters declared previously '''
        self._filters = None
        self._type = None

    def get_filters(self):
        ''' Get current active Filters '''
        return self._filters

    def get_filter_type(self):
        ''' Get Current Filter Type '''
        if self._type is None:
            return "Filters"
        return self._type

    @staticmethod
    def getDoc():
        return "Filters"


# Filter Dependencies for Application
async def app_filter(filterinfo: Optional[List[FilterModel]] = None):
    instance = Filters(filterinfo)
    return instance.get_filters()
