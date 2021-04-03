from pymongo import errors
from mongoengine.errors import InvalidQueryError, LookUpError
from pydantic import BaseModel
from dependencies.exceptions import ModelException


# Declare base model settings
class BaseViewModel(ModelException):
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
    Output = None
    Filter = None
    Ordering = None
    Permission = None
    fields = None
    exclude = None
    SelectRelated = False
    limit = 100
    skip = 0

    def queryset(self):
        ''' Sets QuerySet Objects'''
        queryset = self.Model.objects

        if self.Filter:
            try:
                if isinstance(self.Filter, dict):
                    queryset = queryset.filter(**self.Filter)
                else:
                    queryset = queryset.filter(self.Filter)
            except TypeError:
                raise self.invalid_type('Query')
            except InvalidQueryError:
                raise self.invalid_filter()

        if self.Ordering:
            try:
                queryset = queryset.order_by(*self.Ordering)
            except TypeError:
                raise self.invalid_type('Ordering')
            except AttributeError:
                raise self.invalid_parameter('Ordering')

        if self.fields:
            try:
                queryset = queryset.only(*self.fields)
            except TypeError:
                raise self.invalid_type('fields')
            except AttributeError:
                raise self.invalid_parameter('fields')
            except LookUpError:
                raise self.invalid_field(*self.fields)

        elif self.exclude:
            try:
                queryset = queryset.exclude(*self.exclude)
            except TypeError:
                raise self.invalid_type('exclude')
            except LookupError:
                raise self.invalid_field(*self.exclude)
            except AttributeError:
                raise self.invalid_parameter('exclude')

            queryset = queryset.skip(self.skip).limit(self.limit)

            if self.SelectRelated:
                queryset = queryset.select_related()

            return queryset

    def reset_queryset(self) -> bool:
        ''' Reset QuerySet Objects'''
        self.fields = None
        self.exclude = None
        self.Filter = None
        self.Ordering = None
        self.limit = 0
        self.skip = 0
        self.SelectRelated = False
        return True


# Declare class for Creation of instances
class CreateViewModel(BaseViewModel):
    ''' Declare Create Model Mixin to be inherited '''

    def create(self, data: BaseModel):
        try:
            instance = self.Model(**data.dict())
            instance.save()
        except errors.DuplicateKeyError:
            raise self.already_exist("Model with PrimaryKey")
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
            raise self.not_found(self.Model)

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
            raise self.already_exist(self.Model)
        except self.Model.DoesNotExist:
            raise self.not_found(self.Model)
        except self.Model.MultipleObjectsReturned:
            raise self.multiple_instance_found(self.Model)

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
            instance_model = self.Output(**instance._data)
            patch_data = inward_data.dict(exclude_unset=True)
            patched_instance = instance_model.copy(update=patch_data)
            instance.update(**patched_instance.dict())
        except errors.DuplicateKeyError:
            raise self.already_exist(self.Model)
        except self.Model.DoesNotExist:
            raise self.not_found(self.Model)
        except self.Model.MultipleObjectsReturned:
            raise self.multiple_instance_found(self.Model)

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
            raise self.multiple_instance_found(self.Model)
        except self.Model.DoesNotExist:
            raise self.not_found(self.Model)

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
            raise self.not_found(self.Model)

        return {"status_code": 200, "message": "delete sucessfully"}


class AtomicUpdateViewModel(BaseViewModel):
    ''' Atomic update selected instance.
        All in-bound filters must be valid filter class.
     '''

    def atomic_update(self, Kwargs: dict, data: dict):
        try:
            instance = self.Model.objects(**Kwargs).update(**data)
        except self.Model.DoesNotExist:
            raise self.not_found(self.Model)

        return self.Output(**instance._data)


# Declare ViewSets that inherit all REST operation
class BasicViewSets(GetViewModel,
                    CreateViewModel,
                    ListViewModel,
                    PatchViewModel,
                    DeleteViewModel,
                    AtomicUpdateViewModel
                    ):
    ''' Class provides basic REST operation.
    -get : Get Item based on input parameters.
    -list: Optional Filter Arguments
    -patch: Update non-empty fields in db based on input parameters
    -delete: Delete object instance based on input parameters
    '''
    pass
