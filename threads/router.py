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

    @threads.post("/ratings/{refId}", response_model_exclude_unset=True)
    async def list_ratings(self,
                           refId: str,
                           filters: FilterModel = Depends(app_filter),
                           order_by: SortingModel = Depends(app_ordering),
                           page: PageModel = Depends(pagination)
                           ):
        """ Returns list of available ratings for selected object id.

        Parameters
        ----------
        refId : str
            ReferenceId for Related Model e.g. Product.id.
        filters : FilterModel
            Filtering Parameters
        order_by : SortingModel
            Sorting Parameters
        page : PageModel
            Pagination parameteres

        Returns
        -------
         List of User Ratings

        """

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
        """Short summary.

        Parameters
        ----------
        pk : str
            Primary Unique Key Id.

        Returns
        -------
            Ratings object.

        """
        return self.get({"pk": pk})

    @threads.post("/{thread}/rating/")
    async def create_rating(self,
                            thread: str,
                            rating: RatingsIn,
                            user=Depends(get_active_user)
                            ):
        """Create Ratings for given object.

        Parameters
        ----------
        thread : str
            Type of referenced object i.e. product, place
        rating : RatingsIn
            Ratings Model to store rating

        Returns
        -------
        Instance of newly created rating

        """
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
        """Short summary.

        Parameters
        ----------
        pk : str
            Primary Id of ratings.
        rating : RatingsUpdate
            Update Data Model.

        Returns
        -------
        Updated instance if owner is  current_user

        """
        self.Input = RatingsUpdate
        return self.patch({"pk": pk, "user": user.id}, rating)

    @threads.delete("/rating/{pk}")
    async def delete_rating(self,
                            pk: str,
                            user=Depends(get_active_user)
                            ):
        """Delete the selected instance

        Parameters
        ----------
        pk : str
            Primary Key for instance.
        Returns
        -------
        Success if current_user is the instance.owner

        """
        return self.delete({"pk": pk, "user": user.id})


@cbv(threads)
class CommentsViewModel(BasicViewSets, ListWithOwners):
    '''
    Declaration for Class Based views for Comment Class
    '''

    Model = Comments
    Output = CommentsOut
    Input = CommentsIn

    @threads.post("/comments/{refId}", response_model_exclude_unset=True)
    async def list_comments(self,
                            refId: str,
                            filters: FilterModel = Depends(app_filter),
                            order_by: SortingModel = Depends(app_ordering),
                            page: PageModel = Depends(pagination)
                            ):
        """List comments for objects.

        Parameters
        ----------
        refId : str
            Id of object referenced.
        filters : FilterModel
            Filters to apply
        order_by : SortingModel
            Sorting Orders
        page : PageModel
            Pagination Model

        Returns
        -------
        List all available comments that matches refId and filters

        """

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
        """Get selected comment instance.

        Parameters
        ----------
        pk : str
            Primarykey for Comments

        Returns
        -------
        Instance of comments where pkk matches input pk.

        """
        return self.get({"pk": pk})

    @threads.post("/{thread}/comment")
    async def create_comment(self,
                             thread: str,
                             comment: CommentsIn,
                             user=Depends(get_active_user)
                             ):
        """Create comments for reeferencing models

        Parameters
        ----------
        thread : str
            DType of object referenced
        comment : CommentsIn
            Comment Model for the objects.
        Returns
        -------
        Creates and returns instance of comment if user is active

        """
        # Get Reference Model
        instance = get_reference_model(thread, comment)
        comment.thread = instance
        comment.user = user.id
        return self.create(comment)

    @threads.patch("/comment/{pk}")
    async def patch_comment(self,
                            pk: str,
                            comment: CommentsUpdate,
                            user=Depends(get_active_user)
                            ):
        """Update the comment instance.

        Parameters
        ----------
        pk : str
            Primarykey for comment.
        comment : CommentsUpdate
            Update Data model.

        Returns
        -------
        Updated instance of comments if current user is the owner.

        """
        self.Input = CommentsUpdate
        return self.patch({"pk": pk, "user": user.id}, comment)

    @threads.delete("/comment/{pk}")
    async def delete_comment(self,
                             pk: str,
                             user=Depends(get_active_user)
                             ):
        """Delete Selected instance if user is the owner.

        Parameters
        ----------
        pk : str
            Primary key for the comment.
        Returns
        -------
        Success if deleted i.e. when owner is the user.
        Returns HttpException if user is not the owner

        """
        return self.delete({"pk": pk, "user": user.id})
