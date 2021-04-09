from datetime import datetime
from pydantic import validate_arguments
# import fastapi components
from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import FileResponse
from authentication import get_active_user
from .models import Media
from .serializers import MediaIn, MediaOut
# import ViewSets
from mixin.viewMixin import BasicViewSets, ListWithOwners
from places.router import PlaceViewModel
from items.router import ItemViewModel
from threads.router import RatingsViewModel, CommentsViewModel
from bson.objectid import ObjectId
# Import common dependencies
from dependencies import (cbv,
                          app_filter,
                          FilterModel,
                          ModelException,
                          FileManager
                          )

# Instantiate a API Router for user authentication
media = APIRouter(prefix="",
                  tags=["media"],
                  responses={404: {"description": "Not found"}
                             }
                  )


@validate_arguments
def get_reference_model(thread: str, Id: str):
    ''' Returns Reference View Model'''
    filter = {"pk": Id}
    if thread == "product":
        item = ItemViewModel()
        instance = item.get_instance(filter)
    elif thread == "place":
        place = PlaceViewModel()
        instance = place.get(filter)
    if thread == "rating":
        rating = RatingsViewModel()
        instance = rating.get_instance(filter)
    elif thread == "comment":
        comment = CommentsViewModel()
        instance = comment.get(filter)

    else:
        raise ModelException.not_found("thread: {}".format(thread))

    return instance


@cbv(media)
class MediaViewModel(BasicViewSets, ListWithOwners):
    '''
    Declaration for Class Based views for serializers Class
    '''

    Model = Media
    Output = MediaOut
    Input = MediaIn

    @media.post("/media/{refId}", response_class=FileResponse)
    async def list_media(self,
                         refId: str,
                         filters: FilterModel = Depends(app_filter)
                         ):
        """ Returns list of available ratings for selected object id.

        Parameters
        ----------
        refId : str
            ReferenceId for Related Model e.g. Product.id.
        filters : FilterModel
            Filtering Parameters

        Returns
        -------
         List of User Ratings

        """
        files = []
        self.Filter = filters
        raw_filter = {'thread._ref.$id': ObjectId(refId)}
        self.add_raw_query(raw_filter)
        # Get Media Datas
        medias: list = self.list_detail()

        if not medias:
            raise ModelException.empty_result_info()

        filemanager = FileManager("product")
        for media in medias:
            filemanager.set_context(media.context)
            filemanager.set_content(media.content)
            file = filemanager.get_file(media.filename)
            files.append(file)

        return files

    @media.post("/{context}/media/")
    async def create_media(self,
                           context: str,
                           threadId: str,
                           file: UploadFile = File(...),
                           user=Depends(get_active_user)
                           ):
        """Create meia for given object.

        Parameters
        ----------
        thread : str
            Type of referenced object i.e. product, place
        rating : RatingsIn
            Ratings Model to store media

        Returns
        -------
        Instance of newly created Media Object

        """
        instance = get_reference_model(context, threadId)
        now = datetime.now()
        time = now.strftime("%m%d%Y%H%M%S")
        filename = time + file.filename
        media = MediaIn(filename=filename,
                        content=file.content_type,
                        context=context
                        )
        media.thread = instance
        media.user = user.id
        self.create(media)
        filemanager = FileManager(context)
        await filemanager.save_file(filename, file.file)
        return {"status": 200, "details": filename}

    @media.delete("/{context}/media/")
    async def delete_rating(self,
                            context: str,
                            filename: str,
                            user=Depends(get_active_user)
                            ):
        """Delete the selected instance

        Parameters
        ----------
        context: str,

        pk : str
            Primary Key for instance.

        filename: str
            Name of File to be deleted
        Returns
        -------
        Success if current_user is the instance.owner

        """
        filemanager = FileManager(context)
        filemanager.delete_file(filename)
        return self.delete({"filename": filename, "user": user.id})
