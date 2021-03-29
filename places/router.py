# import common modules
from typing import List
# import fastapi components
from fastapi import APIRouter
from fastapi import Depends # noqa E501
# import fastapi utils for class based views
# from fastapi_utils.cbv import cbv
from dependencies.cbv import cbv
# import custom dependencies
from authentication.oauthprovider import Authenticate # noqa E501
# import custom serializers
from authentication.serializers import ItemBase
from authentication.models import Item
# import ViewSets
from mixin.viewMixin import BasicViewSets
from mongoengine.queryset.visitor import Q  # noqa E501
from dependencies.exceptions import ModelException # noqa E501


# Instantiate a API Router for user authentication
permission = APIRouter(prefix="",
                       tags=["items"],
                       responses={404: {"description": "Not found"}
                                  }
                       )


@cbv(permission)
class ItemViewModel(BasicViewSets):
    '''
    Declaration for Class Based views for serializers Class
    '''

    Model = Item
    Output = ItemBase
    Ordering = ['+product_Id']

    @permission.get("/items", response_model=List[ItemBase])
    async def list_items(self):
        return self.list()

    @permission.get("/item/{item_name}", response_model=ItemBase)
    async def get_item(self, product_Id: str):
        return self.get({"product_Id": product_Id})

    @permission.post("/item/create")
    async def create_item(self, item: ItemBase):
        return self.create(item)

    @permission.post("/item/patch")
    async def patch_item(self, item: ItemBase):
        return self.patch({"product_Id": item.product_Id}, item)

    @permission.post("/item/update")
    async def update_item(self, item: ItemBase):
        return self.put({"product_Id": item.product_Id}, item)
