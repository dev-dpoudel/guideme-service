# import common modules
from datetime import timedelta
from typing import List
# import fastapi components
from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
# import fastapi utils for class based views
# from fastapi_utils.cbv import cbv
from dependencies.cbv import cbv
# import custom dependencies
from config.config import get_settings
# from .oauth import get_active_user, ACCESS_TOKEN_EXPIRE_MINUTES
# from .oauth import get_session, authenticate_user
# from .jsonserver import fake_users_db
from .oauthprovider import Authenticate
# import custom serializers
from .serializers import Token, UserIn, UserOut
from .models import User
# import ViewSets
from mixin.viewMixin import BasicViewSets
from mongoengine.queryset.visitor import Q  # noqa E501
from dependencies.exceptions import not_found  # noqa E501


# Instantiate a API Router for user authentication
user = APIRouter(prefix="/user",
                 tags=["users"],
                 responses={404: {"description": "Not found"}
                            }
                 )


@cbv(user)
class UserViewModel(BasicViewSets):
    '''
    Declaration for Class Based views for serializers Class
    '''

    Model = User
    Output = UserOut
    Ordering = ['-username', 'country']
    # limit = 100
    # skip = 0
    # fields = ['username']
    # Filter = {"username__ne": "alfaaz"}
    # Query = Q(username="alfaaz")

    @user.get("/list", tags=["users", "list"], response_model=List[UserOut])
    async def list_user(self):
        return self.list()

    @user.get("/{username}", tags=["users", "get"], response_model=UserOut)
    async def get_user(self, username: str):
        return self.get({"username": username})

    @user.post("/create", tags=["users", "post"])
    async def create_user(self, user: UserIn):
        return self.create(user)

    @user.post("/update", tags=["users"], response_model=UserOut)
    async def update_password(self, user: UserIn):
        try:
            instance = User.objects.get(username=user.username)
            # Atomic Update Password
            instance.update_one(set__password=user.password)
        except User.DoesNotExist:
            raise not_found("User")

        return UserOut(**instance._data)


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
    # Expire Time for session
    token_expire_time = timedelta(minutes=settings.session_time)
    # Get session data
    session_data = Auth.get_session(
        data={"sub": user.username},
        delta_exp=token_expire_time
    )
    return session_data
