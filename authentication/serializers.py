from typing import Optional, List, Dict
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


# Model for Object Id
class ObjectId(BaseModel):
    oid: str = Field(None,
                     description="Object Id",
                     db_field="$oid"
                     )


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
                          alias="username"
                          )
    # profile: Optional[str] = Field(
    #     None, description="Profile Picture", lt=50
    # )
    first_name: str = Field(None,
                            description="Given Name",
                            max_length=50,
                            alias="firstName",
                            db_field="first_name"
                            )
    last_name: str = Field(None,
                           description="Family Name",
                           max_length=50,
                           alias="lastName"
                           )
    prefered_name: str = Field(None,
                               description="Alias Name",
                               max_length=50,
                               alias="alias"
                               )
    birth_date: datetime = Field(None,
                                 description="Date of Birth",
                                 alias="dob"
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
    email_address: Optional[EmailStr] = Field(
        None,
        description="Email Address",
        alias="emailAddress"
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


# Class for User Creation. Since, on frequent use single user instance is used
class UserIn(UserBase):
    password: str = Field(...,
                          description="User Password",
                          max_length=200
                          )


# User class for read-operation. Multiple records are fetched
class UserOut(UserBase):
    group: List[GroupBase] = Field(None,
                                   description="User Group"
                                   )
    created_date: datetime = Field(None,
                                   description="Created Date",
                                   alias="createdDate"
                                   )
    modified_date: datetime = Field(None,
                                    description="Modified Date",
                                    alias="modifiedDate"
                                    )
    age: Optional[Dict]


# Declare Base Model for JWT Tokens
class Token(BaseModel):
    access_token: str
    token_type: str
    scopes: List[ScopeBase] = []


# Declare Model Calss for Token Data
class TokenData(BaseModel):
    username: Optional[str] = None
