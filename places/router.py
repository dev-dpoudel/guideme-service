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
        self.Filter = filters
        self.Ordering = order_by if order_by else ['+name']
        self.limit = page.limit
        self.skip = page.skip
        return self.list()

    @place.get("/{pk}")
    async def get_place(self,
                        pk: str
                        ):
        return self.get_detail({"pk": pk})

    @place.post("/")
    async def create_place(self,
                           place: PlaceIn,
                           user=Depends(get_active_user)
                           ):
        place.user = user.id
        return self.create(place)

    @place.patch("/{pk}")
    async def patch_place(self,
                          pk: str,
                          place: PlaceUpdate,
                          user=Depends(get_active_user)
                          ):
        self.Input = PlaceUpdate
        return self.patch({"pk": pk, "user": user.id}, place)

    @place.put("/{pk}")
    async def update_place(self,
                           pk: str,
                           place: PlaceIn,
                           user=Depends(get_active_user)
                           ):
        return self.put({"pk": pk, "user": user.id}, place)

    @place.delete("/{pk}")
    async def delete_place(self,
                           pk: str,
                           user=Depends(get_active_user)):
        return self.delete({"pk": pk, "user": user.id})
