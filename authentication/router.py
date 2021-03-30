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
from config.config import get_settings
from .oauthprovider import Authenticate
# import custom serializers
from .serializers import Token, UserBase as UserIn, UserOut
from .models import User
# import ViewSets
from mixin.viewMixin import BasicViewSets
from mongoengine.queryset.visitor import Q  # noqa E501
from dependencies.exceptions import ModelException
from dependencies.filters import app_filter, FilterModel
from dependencies.sorting import app_ordering, SortingModel


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

    @user.post("/list", response_model=List[UserOut])
    async def list_user(self,
                        filters: FilterModel = Depends(app_filter),
                        order_by: SortingModel = Depends(app_ordering)
                        ):

        # Set Filter and Sort Parameters
        self.Filter = filters
        if order_by:
            self.Ordering = order_by
        else:
            self.Ordering = ['+username']
        return self.list()

    @user.get("/{username}", response_model=UserOut)
    async def get_user(self, username: str):
        return self.get({"username": username})

    @user.post("/create")
    async def create_user(self,
                          username: str = Form(...),
                          password: str = Form(...)):

        password = Authenticate.get_hash(password)
        user = UserIn(username=username, password=password)

        return self.create(user)

    @user.put("/update")
    async def update_user(self, user: UserIn):
        return self.patch({"username": user.username}, user)

    @user.post("/update/password")
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
