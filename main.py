# import from typing
# import from fastapi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
# import from pydantic
# Custom written import
from authentication.router import user
from items.router import item


# Instantiate FastAPI instance
# Declare dependencies if any as : dependencies=(dependencyA,dependencyB)
app = FastAPI()

# Declare Authentication Scheme Parameters
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Decleare CORS allowed origins
# List of Allowed host
origins = ["http://localhost",
           "http://localhost:8000",
           ]

# Declare global middlewares to be applied for each request flow
# allowed_methods : Defaults to "GET" apply as list
# max_age : Maximum time in seconds for browser to cache CORS response. 600 def
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=600
)


# Provide router definition for application modules
app.include_router(user)
app.include_router(item)


# Declare a routing function server
@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


# Declare Method with Dependency to use authentication scheme
@app.get("/auth/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}
