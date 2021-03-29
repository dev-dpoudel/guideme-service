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
from .serializers import ProductBase
from .models import Product
# import ViewSets
from mixin.viewMixin import BasicViewSets
from mongoengine.queryset.visitor import Q  # noqa E501
from dependencies.exceptions import ModelException  # noqa E501


# Instantiate a API Router for user authentication
product = APIRouter(prefix="",
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
    Output = ProductBase
    Ordering = ['+product_Id']

    @product.get("/products", response_model=List[ProductBase])
    async def list_items(self):
        return self.list()

    @product.get("/product/{product_Id}", response_model=ProductBase)
    async def get_item(self, product_Id: str):
        return self.get({"product_Id": product_Id})

    @product.post("/product/create")
    async def create_item(self, item: ProductBase):
        return self.create(item)

    @product.post("/product/patch")
    async def patch_item(self, item: ProductBase):
        return self.patch({"product_Id": item.product_Id}, item)

    @product.post("/product/update")
    async def update_item(self, item: ProductBase):
        return self.put({"product_Id": item.product_Id}, item)
