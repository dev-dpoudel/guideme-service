from typing import Optional, List, Dict
from pydantic import BaseModel, Field
from datetime import date, datetime


# Model for User Scope
class ScopeBase(BaseModel):
    menu: str = Field(...,
                      description="Scope Name",
                      max_length=20,
                      )
    permission: str = Field(...,
                            description="Permission Type",
                            max_length=50
                            )


# Model for User Group
class GroupBase(BaseModel):
    name: str = Field(...,
                      description="Group Name",
                      max_length=20
                      )
    menu: List[ScopeBase] = Field(None,
                                  description="Scope List"
                                  )


# Model for User Authentication
class UserBase(BaseModel):
    username: str = Field(...,
                          description="Unique username for user",
                          max_length=20,
                          alias="userName"
                          )
    profile: Optional[float] = Field(
        None, description="Profile Picture", lt=50
    )
    first_name: str = Field(...,
                            description="Given Name",
                            max_length=50,
                            alias="firstName"
                            )
    last_name: str = Field(...,
                           description="Family Name",
                           max_length=50,
                           alias="LastName"
                           )
    prefered_name: str = Field(None,
                               description="Alias Name",
                               max_length=50,
                               alias="Alias"
                               )
    birth_date: date = Field(None,
                             description="Date of Birth",
                             alias="DOB"
                             )
    country: str = Field(None,
                         description="Country",
                         max_length=30
                         )
    city: str = Field(None,
                      description="City",
                      max_length=30
                      )
    zip: str = Field(None,
                     description="Zip Code",
                     max_length=8
                     )
    address: str = Field(None,
                         description="Contact Address",
                         max_length=100
                         )
    perm_address: str = Field(
        None,
        description="Permanent Address",
        max_length=100,
        alias="permanentAddress"
    )
    is_active: bool = Field(
        True,
        description="Is User Active",
        alias="isActive"
    )

    # Configuration Examples
    class Config:
        schema_extra = {
            "example": {
                "username": "alfaaz",
                "first_name": "Dinesh",
                "last_name": "Poudel",
                "prefered_name": "Alfaaz Ryon",
                "birth_date": "1995-01-20",
                "country": "Nepal",
                "city": "kathmandu",
                "zip": "44600",
                "address": "Dhapasi-6,Tokha-6,kathmandu,Nepal",
                "perm_address": "Dhapasi-6,Tokha-6,Kathmandu,Nepal"
            }
        }


# Base user class
class UserPut(UserBase):
    password: str = Field(...,
                          description="User Password",
                          max_length=56
                          )


# Base user class
class UserList(UserBase):
    group: List[GroupBase] = Field(...,
                                   description="User Group"
                                   )
    created_date: datetime = Field(...,
                                   description="Created Date",
                                   alias="createdDate"
                                   )
    modified_date: datetime = Field(...,
                                    description="Modified Date",
                                    alias="modifiedDate"
                                    )
    age: Dict
