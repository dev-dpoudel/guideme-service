# https://github.com/encode/starlette/blob/master/starlette/status.py
from fastapi import HTTPException, status


# Duplicate Key Errors
# pymongo.errors.DuplicateKeyError:
def already_exist(model: str):
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="%s already exist" % (model)
    )


# Define Not Found Status
# <Model>.DoesNotExist
def not_found(model: str):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="%s not found" % (model)
    )


# Define Not Found Status
# <Model>.DoesNotExist
def multiple_instance_found(model: str):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="multiple %s found" % (model)
    )


# Define Not Found Status
# mongoengine.errors.InvalidQueryError
def invalid_filter():
    return HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Invalid Filter Parameters"
    )


# AttributeError
def invalid_parameter(param: str):
    return HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Invalid %s parameter" % (param)
    )


# TypeError
def invalid_type(param: str):
    return HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Type of %s parameter doesn't match" % (param)
    )
