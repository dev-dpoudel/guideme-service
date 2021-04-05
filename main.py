# import profilers
# from fastapi_cprofile.profiler import CProfileMiddleware
# import from mongoengine
from mongoengine import connect, disconnect
# import from typing
# import from fastapi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends
# import from pydantic
# import custom dependencies
from config.config import get_settings, AppSettings
from authentication.oauthprovider import get_active_user
# import custom routers
from authentication.router import user
from permission.router import permission
from items.router import product
from places.router import place
from threads.router import threads

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

# Add Profiling Middlewares
# Cprofile with snakeviz is used currently. File must be with .prof ext
# app.add_middleware(CProfileMiddleware,
#                    enable=True,
#                    server_app=app,
#                    filename='/home/alfaaz/programs/logs/guideme/service.prof',
#                    strip_dirs=False,
#                    sort_by='cumulative')


# Provide router definition for application modules
app.include_router(user)
app.include_router(permission)
app.include_router(product)
app.include_router(place)
app.include_router(threads)


# Declare a startup Event
@app.on_event("startup")
async def startup_event():
    ''' Declare instance for database '''
    settings = get_settings()
    connect(settings.db_name,
            # host=settings.db_host,
            # port=settings.db_port,
            username=settings.db_username,
            password=settings.db_password,
            authentication_source=settings.db_auth_source,
            alias='default'
            )


# Declare a startup Event
@app.on_event("shutdown")
def shutdown_event():
    ''' Declare instance for database '''
    disconnect(alias='default')


# Declare Method with Dependency to use authentication scheme
@app.get("/auth/", tags=['authentication'])
async def read_items(user=Depends(get_active_user)):
    return {"User": user.username}


# Declare Endpoint for app settings and informations
@app.get("/info", tags=['information'])
async def info(settings: AppSettings = Depends(get_settings)):
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "default_page_size": settings.default_page_size,
        "token_active_time": "{0} minutes".format(settings.session_time),
        "db": settings.db_name,
        "db_host": settings.db_host,
        "db_port": settings.db_port,
        "algorithm": settings.algorithm,
        "secret_key": settings.secret_key
    }
