from pydantic import validate_arguments, BaseModel
# import fastapi components
from fastapi import APIRouter, Depends
from authentication import get_active_user
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
from mixin.viewMixin import BasicViewSets, ListWithOwners
from mongoengine.queryset.visitor import Q  # noqa E501
from places.router import PlaceViewModel
from items.router import ItemViewModel
from bson.objectid import ObjectId
# Import common dependencies
from dependencies import (cbv,
                          app_filter,
                          FilterModel,
                          app_ordering,
                          SortingModel,
                          PageModel,
                          pagination,
                          ModelException
                          )

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
class RatingsViewModel(BasicViewSets, ListWithOwners):
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
        return self.list_detail()

    @threads.get("/rating/{pk}")
    async def get_rating(self,
                         pk: str
                         ):
        return self.get({"pk": pk})

    @threads.post("/{thread}/rating/")
    async def create_rating(self,
                            thread: str,
                            rating: RatingsIn,
                            user=Depends(get_active_user)
                            ):
        instance = get_reference_model(thread, rating)
        rating.thread = instance
        rating.user = user.id
        return self.create(rating)

    @threads.patch("/rating/{pk}")
    async def patch_rating(self,
                           pk: str,
                           rating: RatingsUpdate,
                           user=Depends(get_active_user)
                           ):
        self.Input = RatingsUpdate
        return self.patch({"pk": pk, "user": user.id}, rating)

    @threads.put("/rating/{pk}")
    async def update_rating(self,
                            pk: str,
                            rating: RatingsIn,
                            user=Depends(get_active_user)
                            ):
        return self.put({"pk": pk, "user": user.id}, rating)

    @threads.delete("/rating/{pk}")
    async def delete_rating(self,
                            pk: str,
                            user=Depends(get_active_user)
                            ):
        return self.delete({"pk": pk, "user": user.id})


@cbv(threads)
class CommentsViewModel(BasicViewSets, ListWithOwners):
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
        raw_filter = {'thread._ref.$id': ObjectId(refId)}
        self.add_raw_query(raw_filter)
        self.set_page(page)
        self.set_order(order_by, ['+modified_date'])
        # Return Output List
        return self.list_detail()

    @threads.get("/comment/{pk}")
    async def get_comment(self,
                          pk: str
                          ):
        return self.get({"pk": pk})

    @threads.post("/{thread}/comment")
    async def create_comment(self,
                             thread: str,
                             comment: CommentsIn,
                             user=Depends(get_active_user)
                             ):
        # Get Reference Model
        instance = get_reference_model(thread, comment)
        comment.thread = instance
        comment.user = user.id
        return self.create(comment)

    @threads.patch("/comment/{pk}")
    async def patch_rating(self,
                           pk: str,
                           comment: CommentsUpdate,
                           user=Depends(get_active_user)
                           ):
        self.Input = CommentsUpdate
        return self.patch({"pk": pk, "user": user.id}, comment)

    @threads.delete("/comment/{pk}")
    async def delete_rating(self,
                            pk: str,
                            user=Depends(get_active_user)
                            ):
        return self.delete({"pk": pk, "user": user.id})
