from typing import List
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from mixin.baseOutput import BaseOut


# Model for User Group
class GroupBase(BaseModel):
    name: str = Field(...,
                      description="Group Name",
                      max_length=20
                      )
    permission: dict = Field(None,
                             description="Scope Dictionary"
                             )

    # Configuration Examples
    class Config:
        schema_extra = {
            "example": {
                "name": "Admin",
                "permission": {"user": "list get patch"}
            }
        }


class GroupOut(BaseOut, GroupBase):
    pass


# Model for User Authentication
class UserBase(BaseModel):
    username: str = Field(...,
                          description="Unique username for user",
                          max_length=20,
                          )
    # profile: Optional[str] = Field(
    #     None, description="Profile Picture", lt=50
    # )
    first_name: str = Field(None,
                            description="Given Name",
                            max_length=50,
                            )
    last_name: str = Field(None,
                           description="Family Name",
                           max_length=50,
                           )
    prefered_name: str = Field(None,
                               description="Alias Name",
                               max_length=50,
                               )
    birth_date: datetime = Field(None,
                                 description="Date of Birth",
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
    permanent_address: str = Field(None,
                                   description="Permanent Address",
                                   max_length=100,
                                   )
    is_active: bool = Field(True,
                            description="Is User Active",
                            alias="is_active"
                            )
    email_address: EmailStr = Field(None,
                                    description="Email Address",
                                    )

    # Configuration Examples
    class Config:
        schema_extra = {
            "example": {
                "username": "alfaaz",
                "first_name": "Dinesh",
                "last_name": "Poudel",
                "prefered_name": "Alfaaz Ryon",
                "birth_date": "1995-01-20T00:00:00",
                "country": "Nepal",
                "city": "kathmandu",
                "zip": "44600",
                "address": "Dhapasi-6,Tokha-6,kathmandu,Nepal",
                "permanent_address": "Dhapasi-6,Tokha-6,Kathmandu,Nepal",
                "email_address": "testemail@gmail.com",
                "is_active": "True"
            }
        }


# Class for User Creation. Since, on frequent use single user instance is used
class UserIn(UserBase):
    password: str = Field(...,
                          description="User Password",
                          max_length=200
                          )


# User class for read-operation. Multiple records are fetched
class UserOut(BaseOut, UserBase):
    groups: List[str] = Field(None,
                              description="List og assigned groups to user")

    permission: dict = Field(None,
                             description="List of user level permissions")

    modified_date: datetime = Field(None,
                                    description="Modified Date",
                                    )


# Declare Base Model for JWT Tokens
class Token(BaseModel):
    access_token: str
    token_type: str
    scopes: dict
