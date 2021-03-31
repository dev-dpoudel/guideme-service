# import common modules
from typing import List
# import fastapi components
from fastapi import APIRouter
from fastapi import Depends  # noqa E501
# import fastapi utils for class based views
# from fastapi_utils.cbv import cbv
from dependencies.cbv import cbv
# import custom dependencies
from dependencies.exceptions import ModelException  # noqa E501
from dependencies.filters import app_filter, FilterModel
from dependencies.sorting import app_ordering, SortingModel
from dependencies.pagination import PageModel, pagination
# Additioanl dependencies
from authentication.oauthprovider import Authenticate  # noqa E501
# import custom serializers
from authentication.serializers import GroupBase, ScopeBase
from authentication.models import Group, Scope
# import ViewSets
from mixin.viewMixin import BasicViewSets
from mongoengine.queryset.visitor import Q  # noqa E501


# Instantiate a API Router for user authentication
permission = APIRouter(prefix="",
                       tags=["permissions"],
                       responses={404: {"description": "Not found"}
                                  }
                       )


@cbv(permission)
class GroupViewModel(BasicViewSets):
    '''
    Declaration for Class Based views for serializers Class
    '''

    Model = Group
    Output = GroupBase

    @permission.post("/groups", response_model=List[GroupBase])
    async def list_groups(self,
                          filters: FilterModel = Depends(app_filter),
                          order_by: SortingModel = Depends(app_ordering),
                          page: PageModel = Depends(pagination)
                          ):
        self.Filter = filters
        self.Ordering = order_by if order_by else ['+name']
        self.SelectRelated = True
        self.limit = page.limit
        self.skip = page.skip
        return self.list()

    @permission.get("/group/{group_name}", response_model=GroupBase)
    async def get_group(self, group_name: str):
        return self.get({"name": group_name})

    @permission.post("/group/create")
    async def create_group(self, group: GroupBase):
        return self.create(group)

    @permission.put("/group/patch")
    async def patch_group(self, group: GroupBase):
        return self.patch({"name": group.name}, group)

    @permission.post("/group/update")
    async def update_group(self, group: GroupBase):
        return self.put({"name": group.name}, group)


@cbv(permission)
class ScopeViewModel(BasicViewSets):
    '''
    Declaration for Class Based views for Scope
    '''

    Model = Scope
    Output = ScopeBase

    @permission.post("/scopes", response_model=List[ScopeBase])
    async def list_scopes(self,
                          filters: FilterModel = Depends(app_filter),
                          order_by: SortingModel = Depends(app_ordering),
                          page: PageModel = Depends(pagination)
                          ):
        self.Filter = filters
        self.Ordering = order_by if order_by else ['+name']
        self.SelectRelated = True
        self.limit = page.limit
        self.skip = page.skip
        return self.list()

    @permission.get("/scope/{scope_name}", response_model=ScopeBase)
    async def get_group(self, scope_name: str):
        return self.get({"name": scope_name})

    @permission.post("/scope/create")
    async def create_group(self, scope: ScopeBase):
        return self.create(scope)

    @permission.put("/scope/patch")
    async def patch_group(self, scope: ScopeBase):
        return self.patch({"name": scope.name}, scope)

    @permission.post("/scope/update")
    async def update_group(self, scope: ScopeBase):
        return self.put({"name": scope.name}, scope)
