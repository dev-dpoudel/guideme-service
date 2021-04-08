# import fastapi components
from fastapi import APIRouter, Depends
# Additioanl dependencies
from authentication.oauthprovider import is_admin_user
# import custom serializers
from authentication.serializers import GroupBase, GroupOut
from authentication.models import Group
# import ViewSets
from mixin.viewMixin import BasicViewSets
from mongoengine.queryset.visitor import Q  # noqa E501
# import common dependencies
from dependencies import (cbv,
                          app_filter,
                          FilterModel,
                          app_ordering,
                          SortingModel,
                          PageModel,
                          pagination
                          )

# Instantiate a API Router for user authentication
permission = APIRouter(prefix="/group",
                       tags=["permissions"],
                       dependencies=[Depends(is_admin_user)],
                       responses={404: {"description": "Not found"}
                                  }
                       )


@cbv(permission)
class GroupViewModel(BasicViewSets):
    '''
    Declaration for Class Based views for serializers Class
    '''

    Model = Group
    Output = GroupOut
    Input = GroupBase

    @permission.post("s")
    async def list_groups(self,
                          filters: FilterModel = Depends(app_filter),
                          order_by: SortingModel = Depends(app_ordering),
                          page: PageModel = Depends(pagination)
                          ):
        """List available groups.

        Parameters
        ----------
        filters : FilterModel
            Filter model information.
        order_by : SortingModel
            sorting information.
        page : PageModel
            Pagination Information.
        Returns
        -------
        Available list of groups.

        """
        self.Filter = filters
        self.Ordering = order_by if order_by else ['+name']
        self.limit = page.limit
        self.skip = page.skip
        return self.list()

    @permission.get("/{group_name}")
    async def get_group(self, group_name: str):
        """Get Selected Instance of group.

        Parameters
        ----------
        group_name : str
            Group Name.

        Returns
        -------
        List instance of group
        """
        return self.get({"name": group_name})

    @permission.get("/id/{pk}")
    async def get_group_by_Id(self, pk: str):
        """Get Group By Id.

        Parameters
        ----------
        pk : str
            Get instance for the group based on pk.

        Returns
        -------
        Returns group instance if available

        """
        return self.get({"pk": pk})

    @permission.post("/")
    async def create_group(self, group: GroupBase):
        """Create a group instance.

        Parameters
        ----------
        group : GroupBase
            Requested instance of 'group'.

        Returns
        -------
        Instance of group.

        """
        return self.create(group)

    @permission.patch("/")
    async def patch_group(self, group: GroupBase):
        """Update inatance of group.

        Parameters
        ----------
        group : GroupBase
            Update information.

        Returns
        -------
        Updated instance if current user is the admin
        """
        return self.patch({"name": group.name}, group)

    @permission.delete("/{name}")
    async def delete_group(self, name: str):
        """Delete group conntext.

        Parameters
        ----------
        name : str
            Delete instance for the user.

        Returns
        -------
        Success if user is admin else error
        """
        return self.delete({"name": name})
