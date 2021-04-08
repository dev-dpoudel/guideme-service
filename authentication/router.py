# import common modules
from datetime import timedelta
from typing import List
# import fastapi components
from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
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
                          pagination
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

        # Set Filter and Sort Parameters
        self.Filter = filters
        self.Ordering = order_by if order_by else ['+username']
        self.limit = page.limit
        self.skip = page.skip
        return self.list()

    @user.get("/{username}", dependencies=[Depends(is_admin_user)])
    async def get_user(self, username: str):
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

        password = Authenticate.get_hash(password)
        user = UserIn(username=username, password=password)
        return self.create(user)

    @user.patch("/update")
    async def update_user(self,
                          user: UserBase,
                          current_user=Depends(get_current_user)
                          ):
        if current_user.username != user.username:
            return ModelException.access_violation_error()

        return self.patch({"username": user.username}, user)

    @user.delete("/{username}", dependencies=[Depends(is_admin_user)])
    async def delete_user(self, username: str):
        return self.delete({"username": username})

    @user.delete("/")
    async def delete_self(self, user=Depends(get_current_user)):
        return self.delete({"username": user.username})

    @user.post("/password")
    async def update_password(self,
                              user=Depends(get_current_user),
                              old_pass: str = Form(...),
                              password: str = Form(...)
                              ):

        instance = instance = self.get_instance({"username": user.username})

        if not Authenticate.validate_hash(old_pass, instance.password):
            raise Authenticate.InvalidCredentials_exception

        hash = Authenticate.get_hash(password)
        # Atomic Update Password
        instance.update(set__password=hash)

        return {"status": 200, "detial": "Success"}

    @ user.patch("/{username}/group/add",
                 dependencies=[Depends(is_admin_user)]
                 )
    async def add_group(self, username: str, groups: List[str] = Form(...)):
        return self.atomic_update({"username": username},
                                  {"push_all__group": groups}
                                  )

    @ user.patch("/{username}/group/remove",
                 dependencies=[Depends(is_admin_user)]
                 )
    async def remove_group(self, username: str, groups: List[str] = Form(...)):
        return self.atomic_update({"username": username},
                                  {"pull_all__group": groups}
                                  )
