# import common modules
from datetime import timedelta
from typing import List
# import fastapi components
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm
# import fastapi utils for class based views
# from fastapi_utils.cbv import cbv
from dependencies.cbv import cbv
# import custom dependencies
from dependencies.exceptions import ModelException
from dependencies.filters import app_filter, FilterModel
from dependencies.sorting import app_ordering, SortingModel
from dependencies.pagination import PageModel, pagination
# Additional Settings
from config.config import get_settings
from .oauthprovider import Authenticate
# import custom serializers
from .serializers import Token, UserBase, UserIn, UserOut
from .models import User
# import ViewSets
from mixin.viewMixin import BasicViewSets
from mongoengine.queryset.visitor import Q  # noqa E501

# Instantiate a API Router for user authentication
user = APIRouter(prefix="/user",
                 tags=["users"],
                 responses={404: {"description": "Not found"}
                            }
                 )


@user.post("/token", tags=["authenticate"], response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                settings=Depends(get_settings)):

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


@cbv(user)
class UserViewModel(BasicViewSets):
    '''
    Declaration for Class Based views for serializers Class
    '''

    Model = User
    Output = UserOut
    Input = UserBase

    @user.post("/", response_model=List[UserOut])
    async def list_user(self,
                        filters: FilterModel = Depends(app_filter),
                        order_by: SortingModel = Depends(app_ordering),
                        page: PageModel = Depends(pagination)
                        ):

        # Set Filter and Sort Parameters
        self.Filter = filters
        self.Ordering = order_by if order_by else ['+username']
        self.limit = page.limit
        self.skip = page.skip
        return self.list()

    @user.get("/{username}")
    async def get_user(self, username: str):
        try:
            instance = self.Model.objects.get(username=username)
        except self.Model.DoesNotExist:
            raise ModelException.not_found(self.Model)
        # Get Added group and permission level
        groups, permission = instance.scopes
        return self.Output(**instance._data,
                           groups=groups,
                           permission=permission)

    @user.post("/create")
    async def create_user(self,
                          username: str = Form(...),
                          password: str = Form(...)):

        password = Authenticate.get_hash(password)
        user = UserIn(username=username, password=password)
        return self.create(user)

    @user.patch("/update")
    async def update_user(self, user: UserBase):
        return self.patch({"username": user.username}, user)

    @user.delete("/{username}")
    async def delete_user(self, username: str):
        return self.delete({"username": username})

    @user.post("/password")
    async def update_password(self,
                              username: str = Form(...),
                              old_pass: str = Form(...),
                              password: str = Form(...)
                              ):
        try:
            instance = User.objects.get(username=username)
            if not Authenticate.validate_hash(old_pass, instance.password):
                raise Authenticate.InvalidCredentials_exception
            hash = Authenticate.get_hash(password)
            # Atomic Update Password
            instance.update(set__password=hash)
        except User.DoesNotExist:
            raise self.not_found("User")

        return {"status": 200, "detial": "Success"}

    @user.patch("/{username}/group/add")
    async def add_group(self, username: str, groups: List[str] = Form(...)):
        return self.atomic_update({"username": username},
                                  {"push_all__group": groups}
                                  )

    @user.patch("/{username}/group/remove")
    async def remove_group(self, username: str, groups: List[str] = Form(...)):
        return self.atomic_update({"username": username},
                                  {"pull_all__group": groups}
                                  )
