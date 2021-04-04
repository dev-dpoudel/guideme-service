# import common modules
from typing import List
# import fastapi components
from fastapi import APIRouter
from fastapi import Depends  # noqa E501
# import fastapi utils for class based views
# from fastapi_utils.cbv import cbv
from dependencies.cbv import cbv
# import custom dependencies
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
    async def list_items(self):
        return self.list()

    @product.get("/{product_id}", response_model=ProductOut)
    async def get_item(self, product_Id: str):
        return self.get({"pk": product_Id})

    @product.post("/")
    async def create_item(self, item: ProductOut):
        return self.create(item)

    @product.patch("/{product_id}")
    async def patch_item(self, product_id: str, item: ProductIn):
        return self.patch({"pk": product_id}, item)

    @product.put("/{product_id}")
    async def update_item(self, product_id: str, item: ProductIn):
        return self.put({"pk": product_id}, item)

    @product.delete("/{pk}")
    async def delete_place(self, pk: str):
        return self.delete({"pk": pk})
