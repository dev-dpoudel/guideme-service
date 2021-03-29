from datetime import datetime, timedelta
from typing import Optional
# import fastapi libraries
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
# import passlib modules
from passlib.context import CryptContext
# import jwt modules
from jose import JWTError, jwt
# import from custom models
from config.config import get_settings
from .serializers import UserIn, Token
from .models import User

# Following OAUTH Specifiaction tokenUrl is set as token
oauth = OAuth2PasswordBearer(tokenUrl="/user/token")


# Class Instance for OAuth Providers
class Authenticate:
    ''' Create Authentication Class for login Providers
    Allows validation of scopes against logged in users
    '''

    # Declare BcryptContext
    bcrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # Scope for User
    scopes = []

    # Declare credential exception
    InvalidCredentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    InvalidSignature_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Signature has Expired",
    )

    InactiveUser_exception = HTTPException(
        status_code=status.HTTP_417_EXPECTATION_FAILED,
        detail="User is Inactive",
    )

    def __init__(self, **kwargs):

        if kwargs:
            self.SECRET_KEY = kwargs["secret_key"]
            self.ALGORITHM = kwargs["algorithm"]
            self.TOKEN_EXP_TIME = kwargs["token_exp_time"]

    @classmethod
    def get_hash(cls, value: str) -> str:
        '''Return input value as hashed string'''
        return cls.bcrypt.hash(value)

    # Verify Hashed String with corresponding un-hased input
    # Use passlib library context
    @classmethod
    def validate_hash(cls, plain_value: str, hash_value: str) -> bool:
        ''' Validate input hash and plain string are same '''
        return cls.bcrypt.verify(plain_value, hash_value)

    # Return jwt access tokens
    def get_session(self, data: dict, delta_exp: Optional[timedelta] = None):
        ''' Get JWT session data encoded with python-jose '''
        session_input: dict = data.copy()

        # Set Expiration Time
        if delta_exp:
            expire: datetime = datetime.utcnow() + delta_exp
        else:
            expire: datetime = datetime.utcnow() + timedelta(minutes=15)

        # Update expiration time in JWT settings
        session_input.update({"exp": expire})
        # Encode the raw data
        encoded_jwt = jwt.encode(session_input,
                                 self.SECRET_KEY,
                                 algorithm=self.ALGORITHM)

        # Get Session Data
        session = Token(access_token=encoded_jwt,
                        token_type="bearer",
                        scopes=self.scopes
                        )
        return session

    # Authenticate given username and paswword
    def get_user(self, username: str):
        try:
            instance = User.objects.get(username=username)
        except User.DoesNotExist:
            return self.InvalidCredentials_exception

        # Get Pydantic model from the output
        user = UserIn(**instance._data)
        return user

    # Authenticate given username and paswword
    def authenticate_user(self, username: str, password: str):
        ''' get user if available in queryset'''

        # Get Pydantic model from the output
        user = self.get_user(username)

        # Validate Passwords
        if self.validate_hash(password, user.password):
            return user

        raise self.InvalidCredentials_exception

    # Set Username from input Token
    def validate_current_user(self, token):
        try:
            payload = jwt.decode(token,
                                 self.SECRET_KEY,
                                 algorithms=[self.ALGORITHM])

            # set username of current user
            username: str = payload.get("sub")

            # Check if username exists and is set proper
            if username is None:
                raise self.credentials_exception

            # Select user with given username from database
            user = self.get_user(username)
            return user

        # Expired signature error
        except JWTError.ExpiredSignatureError:
            raise self.InvalidSignature_exception

        # Raise Invalid Token Error
        except JWTError.InvalidTokenError:
            raise self.InvalidCredentials_exception


def get_current_user(token: str, settings=Depends(get_settings)):
    ''' Get Current LoggedIn User '''
    Auth = Authenticate(secret_key=settings.secret_key,
                        algorithm=settings.algorithm,
                        token_exp_time=settings.session_time)

    return Auth.validate_current_user(token)


# Get Current Active User
async def get_active_user(current_user: UserIn = Depends(get_current_user)):
    if current_user.is_active:
        return current_user
    else:
        raise HTTPException(status_code=417, detail="User is inactive")
