# import common modules
from datetime import timedelta
from typing import List
# import fastapi components
from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
# import fastapi utils for class based views
# from fastapi_utils.cbv import cbv
from dependencies.cbv import cbv
# import custom dependencies
from .oauth import get_active_user, ACCESS_TOKEN_EXPIRE_MINUTES
from .oauth import get_session, authenticate_user
from .jsonserver import fake_users_db
# import custom serializers
from .serializers import Token, UserIn, UserOut
from .models import User
# import ViewSets
from mongoengine.queryset.visitor import Q  # noqa E501
from dependencies.exceptions import not_found  # noqa E501
from mixin.createMixin import BasicViewSets  # noqa E501

# Instantiate a API Router for user authentication
user = APIRouter(prefix="/user",
                 tags=["users"],
                 responses={404: {"description": "Not found"}
                            }
                 )


@cbv(user)
class UserViewModel():
    # class UserViewModel(BasicViewSets):
    '''
    Declaration for Class Based views for serializers Class
    '''

    Model = User
    Output = UserOut
    # Ordering = ['-username', 'country']
    # limit = 1
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
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Authenticate User Credentials
    user = authenticate_user(fake_users_db,
                             form_data.username,
                             form_data.password
                             )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    session_data = get_session(
        data={"sub": user.username}, delta_exp=access_token_expires
    )
    return session_data


@user.get("/me", response_model=UserIn)
async def read_users_me(current_user: UserIn = Depends(get_active_user)):
    return current_user
