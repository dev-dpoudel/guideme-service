# import common modules
from datetime import timedelta
from typing import List
# import fastapi components
from fastapi import (APIRouter,
                     Depends,
                     Form,
                     File,
                     UploadFile
                     )
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import FileResponse
# Additional Settings
from config.config import get_settings
from .oauthprovider import Authenticate, get_current_user, is_admin_user
# import custom serializers
from .serializers import Token, UserBase, UserIn, UserOut
from .models import User
# import ViewSets
from mixin.viewMixin import BasicViewSets
from mongoengine.queryset.visitor import Q  # noqa E501
# import common dependencies
from dependencies import (cbv,
                          ModelException,
                          app_filter,
                          FilterModel,
                          app_ordering,
                          SortingModel,
                          PageModel,
                          pagination,
                          FileManager
                          )


# Instantiate a API Router for user authentication
user = APIRouter(prefix="/user",
                 tags=["users"],
                 responses={404: {"description": "Not found"}
                            }
                 )


@user.post("/token", tags=["authenticate"], response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                settings=Depends(get_settings)):
    """Authenticate current user.

    Parameters
    ----------
    username : string
        Username of user
    password : string
        password of user
    grant_type: authentication type

    Returns
    -------
    Session token and user scope information

    """

    # User authentication module
    Auth = Authenticate(secret_key=settings.secret_key,
                        algorithm=settings.algorithm,
                        token_exp_time=settings.session_time)

    # Authenticate User Credentials
    user = Auth.authenticate_user(form_data.username,
                                  form_data.password
                                  )

    if not user.username:
        raise ModelException.not_found("User")

    # Expire Time for session
    token_expire_time = timedelta(minutes=settings.session_time)
    # Get session data
    session_data = Auth.get_session(
        data={"sub": user.username},
        delta_exp=token_expire_time
    )
    return session_data


# Get Current Logged In User
@user.get("/me", tags=["authenticate"], response_model=UserOut)
async def me(user=Depends(get_current_user)):
    """Get Details for current logged in user.

    Parameters
    ----------

    Returns
    -------
    Instance of current logged in user
    """
    return user._data


@cbv(user)
class UserViewModel(BasicViewSets):
    '''
    Declaration for Class Based views for serializers Class
    '''

    Model = User
    Output = UserOut
    Input = UserBase

    @user.post("/")
    async def list_user(self,
                        filters: FilterModel = Depends(app_filter),
                        order_by: SortingModel = Depends(app_ordering),
                        page: PageModel = Depends(pagination)
                        ):
        """List all users for application.

        Parameters
        ----------
        filters : FilterModel
            Filter description to be applied.
        order_by : SortingModel
            Sorting Model to be used
        page : PageModel
            Pagination information
        Returns
        -------
        List of available users
        """
        # Set Filter and Sort Parameters
        self.Filter = filters
        self.set_page(page)
        self.set_order(order_by, ['+username'])
        return self.list()

    @user.get("/{username}", dependencies=[Depends(is_admin_user)])
    async def get_user(self, username: str):
        """Get user instance as selected.

        Parameters
        ----------
        username : str
            unique username of user.

        Returns
        -------
        User instance if currentUser is admin
        """
        instance = self.get_instance({"username": username})
        # Get Added group and permission level
        groups, permission = instance.scopes
        return self.Output(**instance._data,
                           groups=groups,
                           permission=permission)

    @user.post("/create")
    async def create_user(self,
                          username: str = Form(...),
                          password: str = Form(...)):
        """Create User Instance.

        Parameters
        ----------
        username : str
            User desired username.
        password : str
            Password for user account.

        Returns
        -------
        Returns instance of newly created user
        """
        password = Authenticate.get_hash(password)
        user = UserIn(username=username, password=password)
        return self.create(user)

    @user.patch("/update")
    async def update_user(self,
                          user: UserBase,
                          current_user=Depends(get_current_user)
                          ):
        """Update input user instance.

        Parameters
        ----------
        user : UserBase
            Selected update data for user.
        Returns
        -------
        Updated user instance if Currentuser is the owner

        """
        if current_user.username != user.username:
            return ModelException.access_violation_error()

        return self.patch({"username": user.username}, user)

    @user.delete("/{username}", dependencies=[Depends(is_admin_user)])
    async def delete_user(self, username: str):
        """Delete given instance.

        Parameters
        ----------
        username : str
            Unique username.

        Returns
        -------
        Success if deleted. CurrentUser Must be admin.
        """
        return self.delete({"username": username})

    @user.delete("/")
    async def delete_self(self, user=Depends(get_current_user)):
        """Delete user account.

        Parameters
        ----------

        Returns
        -------
        Succes message if self. Else HttpException is raised
        """
        return self.delete({"username": user.username})

    @user.post("/password")
    async def update_password(self,
                              user=Depends(get_current_user),
                              old_pass: str = Form(...),
                              password: str = Form(...)
                              ):
        """Update user password

        Parameters
        ----------
        old_pass : str
            Old password.
        password : str
            New Password.

        Returns
        -------
        Success message.

        """

        instance = instance = self.get_instance({"username": user.username})

        if not Authenticate.validate_hash(old_pass, instance.password):
            raise Authenticate.InvalidCredentials_exception

        hash = Authenticate.get_hash(password)
        # Atomic Update Password
        instance.update(set__password=hash)

        return {"status": 200, "detial": "Success"}

    @user.post("/password/set", dependencies=[Depends(is_admin_user)])
    async def set_password(self,
                           username: str = Form(...),
                           password: str = Form(...)
                           ):
        """Set user password. Admin rights needed.

        Parameters
        ----------
        old_pass : str
            Old password.
        password : str
            New Password.

        Returns
        -------
        Success message.

        """
        hash = Authenticate.get_hash(password)
        self.atomic_update({"username": username},
                           {"set__password": hash}
                           )

        return {"status": 200, "detial": "Success"}

    @ user.patch("/{username}/group/add",
                 dependencies=[Depends(is_admin_user)]
                 )
    async def add_group(self, username: str, groups: List[str] = Form(...)):
        """Add group to given user. Admin only.

        Parameters
        ----------
        username : str
            Username selected.
        groups : List[str]
            List of groups to assign user to.

        Returns
        -------
        User instance if user is admin else HttpException.

        """
        return self.atomic_update({"username": username},
                                  {"push_all__group": groups}
                                  )

    @ user.patch("/{username}/group/remove",
                 dependencies=[Depends(is_admin_user)]
                 )
    async def remove_group(self, username: str, groups: List[str] = Form(...)):
        """Remove group from given user. Admin only.

        Parameters
        ----------
        username : str
            Username selected.
        groups : List[str]
            List of groups to remove from user.

        Returns
        -------
        User instance if user is admin else HttpException.

        """
        return self.atomic_update({"username": username},
                                  {"pull_all__group": groups}
                                  )

    @user.post("/image/profile/")
    async def set_profile(self,
                          photo: UploadFile = File(...),
                          user=Depends(get_current_user)
                          ):
        """Set Profile Image for current user

            Parameters
            ----------
            photo : UploadFile
                Profle image for user

            Returns
            -------
                Returns success if sucessful.

            """
        if "image" not in photo.content_type.split("/"):
            raise ModelException.upload_file_error("Please upload image file")

        filemanager = FileManager("profile")
        await filemanager.save_file(photo.filename, photo.file)

        # Update Database Instance
        self.atomic_update({"username": user.username},
                           {"set__profile": photo.filename}
                           )

        return {"status": 200, "details": photo.filename}

    @user.get("/image/profile/{path}", response_class=FileResponse)
    async def get_profile(self,
                          path: str,
                          ):
        """Get Profile Image for current user

        Parameters
        ----------

        Returns
        -------
        Returns profile image for user
        """
        filemanager = FileManager("profile")
        # file = filemanager.get_file(path)
        return filemanager.get_file(path)

    @user.delete("/image/profile/")
    async def unset_profile(self,
                            user=Depends(get_current_user)
                            ):
        """Remove Profile image.

        Parameters
        ----------
        Returns
        -------
            Empty user profile

        """
        filemanager = FileManager("profile")
        filemanager.delete_file(user.profile)
        self.atomic_update({"username": user.username},
                           {"set__profile": None}
                           )

        return {"status": 200, "detial": "Success"}
