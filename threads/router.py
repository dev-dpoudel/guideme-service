from pydantic import validate_arguments, BaseModel
# import fastapi components
from fastapi import APIRouter
from fastapi import Depends  # noqa E501
# import fastapi utils for class based views
# from fastapi_utils.cbv import cbv
from dependencies.cbv import cbv
# import custom dependencies
from dependencies.exceptions import ModelException
from dependencies.filters import app_filter, FilterModel
from dependencies.sorting import app_ordering, SortingModel
from dependencies.pagination import PageModel, pagination
from authentication.oauthprovider import Authenticate  # noqa E501
# import custom serializers
from .serializers import (RatingsOut,
                          RatingsIn,
                          RatingsUpdate,
                          CommentsIn,
                          CommentsOut,
                          CommentsUpdate
                          )
from .models import Ratings, Comments
# import ViewSets
from mixin.viewMixin import BasicViewSets
from mongoengine.queryset.visitor import Q  # noqa E501
from dependencies.exceptions import ModelException  # noqa E501
from places.router import PlaceViewModel
from items.router import ItemViewModel
from bson.objectid import ObjectId


# Instantiate a API Router for user authentication
threads = APIRouter(prefix="",
                    tags=["threads"],
                    responses={404: {"description": "Not found"}
                               }
                    )


@validate_arguments
def get_reference_model(thread: str, entity: BaseModel):
    ''' Returns Reference View Model'''
    if thread == "product":
        item = ItemViewModel()
        instance = item.get_instance({"pk": entity.thread})
    elif thread == "place":
        place = PlaceViewModel()
        instance = place.get({"pk": entity.thread})
    else:
        raise ModelException.not_found("thread: {}".format(thread))

    return instance


@cbv(threads)
class RatingsViewModel(BasicViewSets):
    '''
    Declaration for Class Based views for serializers Class
    '''

    Model = Ratings
    Output = RatingsOut
    Input = RatingsIn

    @threads.post("/ratings/{refId}")
    async def list_ratings(self,
                           refId: str,
                           filters: FilterModel = Depends(app_filter),
                           order_by: SortingModel = Depends(app_ordering),
                           page: PageModel = Depends(pagination)
                           ):

        self.Filter = filters
        raw_filter = {'thread._ref.$id': ObjectId(refId)}
        self.add_raw_query(raw_filter)
        self.set_page(page)
        self.set_order(order_by, ['+name'])
        return self.list()

    @threads.get("/rating/{pk}")
    async def get_rating(self, pk: str):
        return self.get({"pk": pk})

    @threads.post("/{thread}/rating/")
    async def create_rating(self, thread: str, rating: RatingsIn):
        instance = get_reference_model(thread, rating)
        rating.thread = instance
        return self.create(rating)

    @threads.patch("/rating/{pk}")
    async def patch_rating(self, pk: str, rating: RatingsUpdate):
        self.Input = RatingsUpdate
        return self.patch({"pk": pk}, rating)

    @threads.put("/rating/{pk}")
    async def update_rating(self, pk: str,  rating: RatingsIn):
        return self.put({"pk": pk}, rating)

    @threads.delete("/rating/{pk}")
    async def delete_rating(self, pk: str):
        return self.delete({"pk": pk})


@cbv(threads)
class CommentsViewModel(BasicViewSets):
    '''
    Declaration for Class Based views for Comment Class
    '''

    Model = Comments
    Output = CommentsOut
    Input = CommentsIn

    @threads.post("/comments/{refId}")
    async def list_comments(self,
                            refId: str,
                            filters: FilterModel = Depends(app_filter),
                            order_by: SortingModel = Depends(app_ordering),
                            page: PageModel = Depends(pagination)
                            ):

        # Apply incomming filter. Append raw filters
        self.Filter = filters
        # raw_filter = {'thread._ref.$id': ObjectId(refId)}
        raw_filter = ""
        self.add_raw_query(raw_filter)
        self.set_page(page)
        self.set_order(order_by, ['+modified_date'])
        # Return Output List
        return self.list()

    @threads.get("/comment/{pk}")
    async def get_comment(self, pk: str):
        return self.get({"pk": pk})

    @threads.post("/{thread}/comment")
    async def create_comment(self, thread: str, comment: CommentsIn):
        instance = get_reference_model(thread, comment)
        comment.thread = instance
        return self.create(comment)

    @threads.patch("/comment/{pk}")
    async def patch_rating(self, pk: str, comment: CommentsUpdate):
        self.Input = CommentsUpdate
        return self.patch({"pk": pk}, comment)

    @threads.delete("/comment/{pk}")
    async def delete_rating(self, pk: str):
        return self.delete({"pk": pk})
