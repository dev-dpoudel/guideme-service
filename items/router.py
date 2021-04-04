# import common modules
from typing import List
# import fastapi components
from fastapi import APIRouter
from fastapi import Depends  # noqa E501
# import fastapi utils for class based views
# from fastapi_utils.cbv import cbv
from dependencies.cbv import cbv
# import custom dependencies
from dependencies.filters import app_filter, FilterModel
from dependencies.sorting import app_ordering, SortingModel
from dependencies.pagination import PageModel, pagination
from authentication.oauthprovider import Authenticate  # noqa E501
# import custom serializers
from .serializers import ProductIn, ProductOut
from .models import Product
# import ViewSets
from mixin.viewMixin import BasicViewSets
from mongoengine.queryset.visitor import Q  # noqa E501
from dependencies.exceptions import ModelException  # noqa E501


# Instantiate a API Router for user authentication
product = APIRouter(prefix="/product",
                    tags=["products"],
                    responses={404: {"description": "Not found"}
                               }
                    )


@cbv(product)
class ItemViewModel(BasicViewSets):
    '''
    Declaration for Class Based views for Item serializers Class
    '''

    Model = Product
    Output = ProductOut
    Input = ProductIn
    Ordering = ['+name']

    @product.post("s", response_model=List[ProductOut])
    async def list_items(self,
                         filters: FilterModel = Depends(app_filter),
                         order_by: SortingModel = Depends(app_ordering),
                         page: PageModel = Depends(pagination)
                         ):
        self.Filter = filters
        self.Ordering = order_by if order_by else ['+name']
        self.limit = page.limit
        self.skip = page.skip
        return self.list()

    @product.get("/{pk}", response_model=ProductOut)
    async def get_item(self, pk: str):
        return self.get({"pk": pk})

    @product.post("/")
    async def create_item(self, item: ProductOut):
        return self.create(item)

    @product.patch("/{pk}")
    async def patch_item(self, pk: str, item: ProductIn):
        return self.patch({"pk": pk}, item)

    @product.put("/{pk}")
    async def update_item(self, pk: str, item: ProductIn):
        return self.put({"pk": pk}, item)

    @product.delete("/{pk}")
    async def delete_place(self, pk: str):
        return self.delete({"pk": pk})
