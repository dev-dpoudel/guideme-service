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
from .serializers import PlaceIn, PlaceOut
from .models import Place
# import ViewSets
from mixin.viewMixin import BasicViewSets
from mongoengine.queryset.visitor import Q  # noqa E501
from dependencies.exceptions import ModelException  # noqa E501


# Instantiate a API Router for user authentication
place = APIRouter(prefix="/place",
                  tags=["places"],
                  responses={404: {"description": "Not found"}
                             }
                  )


@cbv(place)
class ItemViewModel(BasicViewSets):
    '''
    Declaration for Class Based views for serializers Class
    '''

    Model = Place
    Output = PlaceOut
    Input = PlaceIn
    Ordering = ['+name']

    @place.post("s", response_model=List[PlaceOut])
    async def list_places(self):
        return self.list()

    @place.get("/{pk}")
    async def get_place(self, pk: str):
        return self.get({"pk": pk})

    @place.post("/")
    async def create_place(self, place: PlaceIn):
        return self.create(place)

    @place.patch("/{pk}")
    async def patch_place(self, pk: str, place: PlaceIn):
        return self.patch({"pk": pk}, place)

    @place.put("/{pk}")
    async def update_place(self, pk: str, place: PlaceIn):
        return self.put({"pk": pk}, place)

    @place.delete("/{pk}")
    async def delete_place(self, pk: str):
        return self.delete({"pk": pk})
