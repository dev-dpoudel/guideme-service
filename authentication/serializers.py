from typing import List
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from mixin.baseOutput import BaseOut


# Model for User Scope
class ScopeBase(BaseOut):
    menu: str = Field(...,
                      description="Scope Name",
                      max_length=20,
                      )
    permission: str = Field(...,
                            description="Permission Type",
                            max_length=50
                            )


# Model for User Group
class GroupBase(BaseOut):
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
                "birth_Date": "1995-01-20",
                "country": "Nepal",
                "city": "kathmandu",
                "zip": "44600",
                "address": "Dhapasi-6,Tokha-6,kathmandu,Nepal",
                "permanent_address": "Dhapasi-6,Tokha-6,Kathmandu,Nepal",
                "email_address": "",
                "is_active": ""
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
    group: List[GroupBase] = Field(None,
                                   description="User Group"
                                   )
    created_date: datetime = Field(None,
                                   description="Created Date",
                                   )
    modified_date: datetime = Field(None,
                                    description="Modified Date",
                                    )


# Declare Base Model for JWT Tokens
class Token(BaseModel):
    access_token: str
    token_type: str
    scopes: List[ScopeBase] = []
