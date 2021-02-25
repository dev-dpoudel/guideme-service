# import from typing
# import from fastapi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# import from pydantic
# Custom written import
from authentication.router import user
from items.router import item


# Instantiate FastAPI instance
# Declare dependencies if any as : dependencies=(dependencyA,dependencyB)
app = FastAPI()

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
