from pymongo import errors
from mongoengine.errors import InvalidQueryError
from pydantic import BaseModel
from dependencies.exceptions import (already_exist,
                                     not_found,
                                     multiple_instance_found,
                                     invalid_filter,
                                     invalid_parameter,
                                     invalid_type
                                     )


# Declare base model settings
class BaseViewModel:
    '''
        Basic View Model instance
        Query : Q object instance
        Filter : Dictionary with key value pairs
        Ordering: List of Orderby Fields
        fields: Field to get from document
        exclude: Fields to exculde from queryset
        Permission: Check Permission for each operation
        limit : Maximum number of records returned from docs. 0 means all
        skip: No of records to skip
    '''
    Model = None
    Output: BaseModel = None
    Input: BaseModel = None
    Query = None
    Filter: dict = None
    Ordering: list = None
    Permission: list = None
    fields: list = None
    exclude: list = None
    limit: int = 100
    skip: int = 0

    def queryset(self):
        ''' Sets QuerySet Objects'''
        queryset = self.Model.objects

        if self.Filter:
            try:
                queryset = queryset.filter(**self.Filter)
            except TypeError:
                raise invalid_type('Filter')
            except InvalidQueryError:
                raise invalid_filter()

        elif self.Query:
            try:
                queryset = queryset.filter(self.Query)
            except TypeError:
                raise invalid_type('Query')
            except InvalidQueryError:
                raise invalid_filter()

        if self.Ordering:
            try:
                queryset = queryset.order_by(*self.Ordering)
            except TypeError:
                raise invalid_type('Ordering')
            except AttributeError:
                raise invalid_parameter('Ordering')

        if self.fields:
            try:
                queryset = queryset.only(*self.fields)
            except TypeError:
                raise invalid_type('fields')
            except AttributeError:
                raise invalid_parameter('fields')

        elif self.exclude:
            try:
                queryset = queryset.exclude(*self.exclude)
            except TypeError:
                raise invalid_type('exclude')
            except AttributeError:
                raise invalid_parameter('exclude')

        return queryset.skip(self.skip).limit(self.limit)

    def reset_queryset(self) -> bool:
        ''' Reset QuerySet Objects'''
        self.fields = None
        self.exclude = None
        self.Filter = None
        self.Query = None
        self.Ordering = None
        self.limit = 0
        self.skip = 0
        return True


# Declare class for Creation of instances
class CreateViewModel(BaseViewModel):
    ''' Declare Create Model Mixin to be inherited '''

    def create(self, data: BaseModel):
        try:
            instance = self.Model(**data.dict())
            instance.save()
        except errors.DuplicateKeyError:
            raise already_exist("Model with PrimaryKey")
        return self.Output(**instance._data)


# Declare Class to get specific Instance.
class GetViewModel(BaseViewModel):
    ''' Get Mixin.
        Use of primary key is mandatory.
        Returns Error in case of multiple values or DoesNotExist.
        May use multiple filter parameters
    '''

    def get(self, Kwargs: dict):
        try:
            instance = self.queryset().get(**Kwargs)
        except self.Model.DoesNotExist:
            raise not_found(self.Model)

        return self.Output(**instance._data)


# Declare Class to List all available instances. Use of filters supported
class ListViewModel(BaseViewModel):
    ''' List All Available instances.
        Use of filter class for filtering objects.
        All in-bound filters must be valid filter class
     '''

    def list(self):
        models = self.queryset()
        model_data = [model._data for model in models]
        return model_data


# Declare Class to Replace existing instances.
class UpdateViewModel(BaseViewModel):
    ''' Replace selected instances.
        Update is used to guarantee replacing of entire object fields.
        All in-bound filters must be valid filter class.
     '''

    def put(self, Kwargs: dict, inward_data: BaseModel):
        try:
            instance = self.queryset().get(**Kwargs)
            instance.update(**inward_data.dict())
        except errors.DuplicateKeyError:
            raise already_exist(self.Model)
        except self.Model.DoesNotExist:
            raise not_found(self.Model)
        except self.Model.MultipleObjectsReturned:
            raise multiple_instance_found(self.Model)

        return self.Output(**instance._data)


# Declare Class to Update existing instance.
class PatchViewModel(BaseViewModel):
    ''' Update selected instances.
        Partial update is used to guarantee update of only desired fields.
        All in-bound filters must be valid filter class.
     '''

    def patch(self, Kwargs: dict, inward_data: BaseModel):
        try:
            instance = self.queryset().get(**Kwargs)
            instance_model = self.Model(**instance._data)
            patch_data = inward_data.dict(exclude_unset=True)
            patched_instance = instance_model.copy(update=patch_data)
            instance.update(**patched_instance.dict())
        except errors.DuplicateKeyError:
            raise already_exist(self.Model)
        except self.Model.DoesNotExist:
            raise not_found(self.Model)
        except self.Model.MultipleObjectsReturned:
            raise multiple_instance_found(self.Model)

        return self.Output(**instance._data)


# Declare Class to Delete existing instances.
class DeleteViewModel(BaseViewModel):
    ''' Delete selected instance.
        All in-bound filters must be valid filter class.
     '''

    def delete(self, Kwargs: dict):
        try:
            instance = self.queryset().get(**Kwargs)
            instance.delete()
        except self.Model.MultipleObjectsReturned:
            raise multiple_instance_found(self.Model)
        except self.Model.DoesNotExist:
            raise not_found(self.Model)

        return {"status_code": 200, "message": "delete sucessfully"}


# Declare Class to Delete existing instances.
class DeleteMultipleViewModel(BaseViewModel):
    ''' Bulk Delete selected instance.
        All in-bound filters must be valid filter class.
     '''

    def bulkdelete(self):
        try:
            instance = self.queryset()
            instance.delete()
        except self.Model.DoesNotExist:
            raise not_found(self.Model)

        return {"status_code": 200, "message": "delete sucessfully"}


# Declare ViewSets that inherit all REST operation
class BasicViewSets(GetViewModel,
                    CreateViewModel,
                    ListViewModel,
                    PatchViewModel,
                    DeleteViewModel):
    ''' Class provides basic REST operation.
    -get : Get Item based on input parameters.
    -list: Optional Filter Arguments
    -patch: Update non-empty fields in db based on input parameters
    -delete: Delete object instance based on input parameters
    '''
    pass
