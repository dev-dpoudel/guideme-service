# import fastapi components
from fastapi import APIRouter, Depends
from authentication import get_active_user
# import custom serializers
from .serializers import ProductIn, ProductOut, ProductUpdate
from .models import Product
# import ViewSets
from mixin.viewMixin import BasicViewSets, UpdateViewModel, GetWithOwners
from mongoengine.queryset.visitor import Q  # noqa E501
# Import common dependencies
from dependencies import (cbv,
                          app_filter,
                          FilterModel,
                          app_ordering,
                          SortingModel,
                          PageModel,
                          pagination
                          )

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
        """Get list of all available products.

        Parameters
        ----------
        filters : FilterModel
            Filter parameteres
        order_by : SortingModel
            Sorting Parameters
        page : PageModel
            Pagination Information

        Returns
        -------
        List of available products that matches input filter parameters.

        """
        self.Filter = filters
        self.Ordering = order_by if order_by else ['+name']
        self.limit = page.limit
        self.skip = page.skip
        return self.list()

    @product.get("/{pk}")
    async def get_item(self,
                       pk: str
                       ):
        """Select a distinct product with primarykey.

        Parameters
        ----------
        pk : str
            Get item with reference to primary key.

        Returns
        -------
        Distinct instance of product if available

        """
        return self.get_detail({"pk": pk})

    @product.post("/")
    async def create_item(self,
                          item: ProductIn,
                          user=Depends(get_active_user)
                          ):
        """Create items as requested by user.

        Parameters
        ----------
        item : ProductIn
            item model information

        Returns
        -------
        Newly created instance if user is active.

        """
        item.user = user.id
        return self.create(item)

    @product.patch("/{pk}")
    async def patch_item(self,
                         pk: str,
                         item: ProductUpdate,
                         user=Depends(get_active_user)
                         ):
        """Update the selected items.

        Parameters
        ----------
        pk : str
            Primary key for specific instance.
        item : ProductUpdate
            Updated information for product.

        Returns
        -------
        Updated instance of product if user is the owner of instance..
        """
        self.Input = ProductUpdate
        return self.patch({"pk": pk, "user": user.id}, item)

    @product.put("/{pk}")
    async def update_item(self,
                          pk: str,
                          item: ProductIn,
                          user=Depends(get_active_user)
                          ):
        """Replace Items.

        Parameters
        ----------
        pk : str
            Primarykey for instance.
        item : ProductIn
            Information for items.

        Returns
        -------
        def
            Returns updated instance if user is the owner of instance.

        """
        return self.put({"pk": pk, "user": user.id}, item)

    @product.delete("/{pk}")
    async def delete_place(self,
                           pk: str,
                           user=Depends(get_active_user)
                           ):
        """Delete selected instance.

        Parameters
        ----------
        pk : str
            Primarykey for the instance.

        Returns
        -------
        Returns Success if user is the owner of instance.
        """
        return self.delete({"pk": pk, "user": user.id})
