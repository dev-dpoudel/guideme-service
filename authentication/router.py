from fastapi import APIRouter

# Instantiate a API Router for user authentication
user = APIRouter()


@user.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@user.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@user.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
