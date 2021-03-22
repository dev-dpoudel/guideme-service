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
from .serializers import UserIn, TokenData, Token, ScopeBase
from .jsonserver import fake_users_db, fake_scope_db

# The key is unique and has to be kept private. openssl rand -hex 32
SECRET_KEY = "1f2d98baf9dbd390b97a9750689297b12ea71fb6859219a797e1da111714b947"
# Declare JWT Hashing ALGORITHM
ALGORITHM = "HS256"
# Session expiry time in minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 15

# Declare Authentication Scheme Parameters
# Following OAUTH Specifiaction tokenUrl is set as token
oauth = OAuth2PasswordBearer(tokenUrl="token")

# Declare BcryptContext
bcrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Define hash function for global use
# Use passlib library context
def get_hash(value: str) -> str:
    ''' Return input value as hased string '''
    return bcrypt.hash(value)


# Verify Hashed String with corresponding un-hased input
# Use passlib library context
def validate_hash(plain_value: str, hash_value: str) -> bool:
    ''' Validate input hash and plain string are same '''
    return bcrypt.verify(plain_value, hash_value)


# Define function to get session tokens
def get_session(data: dict, delta_exp: Optional[timedelta] = None):
    ''' Get JWT session data encoded with python-jose '''
    raw_data: dict = data.copy()

    # Set Expiration Time
    if delta_exp:
        expire: datetime = datetime.utcnow() + delta_exp
    else:
        expire: datetime = datetime.utcnow() + timedelta(minutes=15)

    # Update expiration time in JWT settings
    raw_data.update({"exp": expire})
    # Encode the raw data
    encoded_jwt = jwt.encode(raw_data,
                             SECRET_KEY,
                             algorithm=ALGORITHM)
    # Get Session Data
    session = Token(access_token=encoded_jwt,
                    token_type="bearer",
                    scopes=get_scopes(fake_scope_db, data["sub"])
                    )
    return session


# Get Selected UserIn
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserIn(**user_dict)


# Authenticate given username and paswword
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not validate_hash(password, user.password):
        return False
    return user


# Authenticate given username and paswword
def get_scopes(scope_db, username: str):
    scopes = []
    scopes.append(ScopeBase(menu="Dahboard", permission="read write"))
    return scopes


# Get Current Loggedin UserIn
async def get_current_user(token: str = Depends(oauth)):
    ''' Get Current LoggedIn UserIn '''
    # Declare credential exception
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    # Select user with given username from database
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


# Get Current Active UserIn
async def get_active_user(current_user: UserIn = Depends(get_current_user)):
    if current_user.is_active:
        return current_user
    else:
        raise HTTPException(status_code=400, detail="UserIn is inactive")
