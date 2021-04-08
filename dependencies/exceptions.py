# https://github.com/encode/starlette/blob/master/starlette/status.py
from fastapi import HTTPException, status


class ModelException:
    # Duplicate Key Errors
    # pymongo.errors.DuplicateKeyError:
    @staticmethod
    def already_exist(model: str):
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="%s already exist" % (model)
        )

    # Define Not Found Status
    # <Model>.DoesNotExist
    @staticmethod
    def not_found(model: str):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="%s not found" % (model)
        )

    # Define Not Found Status
    # <Model>.DoesNotExist
    @staticmethod
    def multiple_instance_found(model: str):
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="multiple %s found" % (model)
        )

    # Define Not Found Status
    # mongoengine.errors.InvalidQueryError
    @staticmethod
    def invalid_filter():
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid Filter Parameters"
        )

    # AttributeError
    @staticmethod
    def invalid_parameter(param: str):
        return HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail="Invalid %s parameter" % (param)
        )

    # TypeError
    @staticmethod
    def invalid_type(param: str):
        return HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail="Type of %s parameter doesn't match" % (param)
        )

    # LookupError
    @staticmethod
    def invalid_field(param: str):
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Field %s doesn't exist on database" % (param)
        )

    @staticmethod
    def validation_error(error: str):
        return HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail=error.errors()
        )

    @staticmethod
    def access_violation_error(error: str):
        return HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Access Violation Error"
        )
