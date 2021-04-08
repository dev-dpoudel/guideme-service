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
from authentication.oauthprovider import get_active_user
# import custom serializers
from .serializers import ProductIn, ProductOut, ProductUpdate
from .models import Product
# import ViewSets
from mixin.viewMixin import BasicViewSets, UpdateViewModel, GetWithOwners
from mongoengine.queryset.visitor import Q  # noqa E501
from dependencies.exceptions import ModelException  # noqa E501


# Instantiate a API Router for user authentication
product = APIRouter(prefix="/product",
                    tags=["products"],
                    responses={404: {"description": "Not found"}
                               }
                    )


@cbv(product)
class ItemViewModel(BasicViewSets, UpdateViewModel, GetWithOwners):
    '''
    Declaration for Class Based views for Item serializers Class
    '''

    Model = Product
    Output = ProductOut
    Input = ProductIn
    Ordering = ['+name']

    @product.post("s")
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

    @product.get("/{pk}")
    async def get_item(self, pk: str):
        return self.get_detail({"pk": pk})

    @product.post("/")
    async def create_item(self,
                          item: ProductIn,
                          user=Depends(get_active_user)
                          ):
        item.user = user.id
        return self.create(item)

    @product.patch("/{pk}")
    async def patch_item(self,
                         pk: str,
                         item: ProductUpdate,
                         user=Depends(get_active_user)
                         ):
        self.Input = ProductUpdate
        return self.patch({"pk": pk, "user": user.id}, item)

    @product.put("/{pk}")
    async def update_item(self,
                          pk: str,
                          item: ProductIn,
                          user=Depends(get_active_user)
                          ):
        return self.put({"pk": pk, "user": user.id}, item)

    @product.delete("/{pk}")
    async def delete_place(self,
                           pk: str,
                           user=Depends(get_active_user)
                           ):
        return self.delete({"pk": pk, "user": user.id})
