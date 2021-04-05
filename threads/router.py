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
from .serializers import RatingsOut, RatingsIn, CommentsIn, CommentsOut
from .models import Ratings, Comments
# import ViewSets
from mixin.viewMixin import BasicViewSets
from mongoengine.queryset.visitor import Q  # noqa E501
from dependencies.exceptions import ModelException  # noqa E501


# Instantiate a API Router for user authentication
threads = APIRouter(prefix="",
                    tags=["threads"],
                    responses={404: {"description": "Not found"}
                               }
                    )


@cbv(threads)
class RatingsViewModel(BasicViewSets):
    '''
    Declaration for Class Based views for serializers Class
    '''

    Model = Ratings
    Output = RatingsOut
    Input = RatingsIn

    @threads.post("/ratings")
    async def list_ratings(self,
                           filters: FilterModel = Depends(app_filter),
                           order_by: SortingModel = Depends(app_ordering),
                           page: PageModel = Depends(pagination)
                           ):
        self.Filter = filters
        self.Ordering = order_by if order_by else ['+name']
        self.limit = page.limit
        self.skip = page.skip
        return self.list()

    @threads.get("/rating/{pk}")
    async def get_rating(self, pk: str):
        return self.get({"pk": pk})

    @threads.post("/rating/")
    async def create_rating(self, rating: RatingsIn):
        return self.create(rating)

    @threads.patch("/rating/{pk}")
    async def patch_rating(self, pk: str, rating: RatingsIn):
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

    @threads.post("/comments")
    async def list_comments(self,
                            filters: FilterModel = Depends(app_filter),
                            order_by: SortingModel = Depends(app_ordering),
                            page: PageModel = Depends(pagination)
                            ):
        self.Filter = filters
        self.Ordering = order_by if order_by else ['+modified_date']
        self.limit = page.limit
        self.skip = page.skip
        return self.list()

    @threads.get("/comment/{pk}")
    async def get_comment(self, pk: str):
        return self.get({"pk": pk})

    @threads.post("/comment")
    async def create_comment(self, comment: CommentsIn):
        return self.create(comment)

    @threads.patch("/comment/{pk}")
    async def patch_rating(self, pk: str, comment: CommentsIn):
        return self.patch({"pk": pk}, comment)

    @threads.put("/comment/{pk}")
    async def update_rating(self, pk: str,  comment: CommentsIn):
        return self.put({"pk": pk}, comment)

    @threads.delete("/comment/{pk}")
    async def delete_rating(self, pk: str):
        return self.delete({"pk": pk})
