# import fastapi components
from fastapi import APIRouter
from fastapi import Depends  # noqa E501
# import custom serializers
from authentication import get_active_user
from .serializers import PlaceIn, PlaceOut, PlaceUpdate
from .models import Place
# import ViewSets
from mixin.viewMixin import BasicViewSets, GetWithOwners
from mongoengine.queryset.visitor import Q  # noqa E501
from dependencies import (cbv,
                          app_filter,
                          FilterModel,
                          app_ordering,
                          SortingModel,
                          PageModel,
                          pagination
                          )


# Instantiate a API Router for user authentication
place = APIRouter(prefix="/place",
                  tags=["places"],
                  responses={404: {"description": "Not found"}
                             }
                  )


@cbv(place)
class PlaceViewModel(BasicViewSets, GetWithOwners):
    '''
    Declaration for Class Based views for serializers Class
    '''

    Model = Place
    Output = PlaceOut
    Input = PlaceIn
    Ordering = ['+name']

    @place.post("s")
    async def list_places(self,
                          filters: FilterModel = Depends(app_filter),
                          order_by: SortingModel = Depends(app_ordering),
                          page: PageModel = Depends(pagination)
                          ):
        """Get List of available places.

        Parameters
        ----------
        filters : FilterModel
            Filter to be applied.
        order_by : SortingModel
            Ordering Models
        page : PageModel
            Pagination information
        Returns
        -------
        List of available places based on filters.

        """
        self.Filter = filters
        self.Ordering = order_by if order_by else ['+name']
        self.limit = page.limit
        self.skip = page.skip
        return self.list()

    @place.get("/{pk}")
    async def get_place(self,
                        pk: str
                        ):
        """Get selected places.

        Parameters
        ----------
        pk : str
            Primary key for places.

        Returns
        -------
        Instance of place selected per place
        """
        return self.get_detail({"pk": pk})

    @place.post("/")
    async def create_place(self,
                           place: PlaceIn,
                           user=Depends(get_active_user)
                           ):
        """Creates place instance as requested.

        Parameters
        ----------
        place : PlaceIn
            Place instance requested for users.

        Returns
        -------
        Newly created instance if user is active.
        """
        place.user = user.id
        return self.create(place)

    @place.patch("/{pk}")
    async def patch_place(self,
                          pk: str,
                          place: PlaceUpdate,
                          user=Depends(get_active_user)
                          ):
        """Update place instance.

        Parameters
        ----------
        pk : str
            Primary key for selected instance.
        place : PlaceUpdate
            Update model for place.

        Returns
        -------
        Returns updated instance for place if user is the owner
        """
        self.Input = PlaceUpdate
        return self.patch({"pk": pk, "user": user.id}, place)

    @place.put("/{pk}")
    async def update_place(self,
                           pk: str,
                           place: PlaceIn,
                           user=Depends(get_active_user)
                           ):
        """Returns updated place.

        Parameters
        ----------
        pk : str
            Primartkey for the selected instance.
        place : PlaceIn
            Update instance for place.

        Returns
        -------
        Returns updated instance if user is the owner.

        """
        return self.put({"pk": pk, "user": user.id}, place)

    @place.delete("/{pk}")
    async def delete_place(self,
                           pk: str,
                           user=Depends(get_active_user)):
        """Delete instance if owner is the user.

        Parameters
        ----------
        pk : str
            Primary Key for place instance.

        Returns
        -------
        Returns success if place owner is the current user
        """
        return self.delete({"pk": pk, "user": user.id})
