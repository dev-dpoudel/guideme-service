from mongoengine import Document
from mongoengine import fields as Field
from mongoengine import PULL
from datetime import datetime


# User document for login informations
class User(Document):
    # Username for the current user
    username = Field.StringField(
        help_text="Unique Username",
        required=True,
        primary_key=True,
        unique=True,
        max_length=20
    )

    # Password for the username
    password = Field.StringField(
        help_text="Password : Hashed",
        required=True,
        primary_key=True,
        unique=True,
        max_length=56
    )

    # User Profile Image
    profile = Field.ImageField(
        help_text="Profile Image",
        null=True
    )

    # User associated groups
    group = Field.ListField(
        Field.LazyReferenceField('Group', reverse_delete_rule=PULL),
        help_text="Assigned User Groups",
        default=list,
        null=True
    )

    # Username for the user
    first_name = Field.StringField(
        help_text="First Name of the user",
        max_length=50
    )
    # Surname of the user
    last_name = Field.StringField(
        help_text="Last Name of the User",
        max_length=50
    )
    # Prefered Name of user
    prefered_name = Field.StringField(
        help_text="Prefered Name of the user",
        max_length=20,
        null=True
    )
    # Birthdate
    birth_date = Field.DateTimeField(
        help_text="Birthdate of the User",
        null=True
    )
    # Nationality
    country = Field.StringField(
        help_text="Country",
        max_length=30,
        null=True
    )
    # City
    city = Field.StringField(
        help_text="City",
        max_length=30,
        null=True
    )
    # Postal/Zip Code
    zip = Field.StringField(
        help_text="Zip Code",
        max_length=8,
        null=True
    )
    # Current Address
    address = Field.StringField(
        help_text="Contact Address",
        max_length=100,
        null=True
    )
    # Permanent Address
    perm_address = Field.StringField(
        help_text="Permanent Address",
        max_length=100,
        null=True
    )
    # User status
    is_active = Field.BooleanField(
        help_text="Is User Active",
        defult=True
    )
    # Registered Date
    created_date = Field.DateTimeField(
        help_text="User Created Date",
        default=datetime.utcnow()
    )
    modified_date = Field.DateTimeField(
        help_text="Last Modification Date",
        default=datetime.utcnow()
    )
    meta = {'collection': 'users'}


# User document for permission informations
class Group(Document):
    ''' Defines User Group for Operations'''
    # Name of the group
    name = Field.StringField(
        help_text="Name of the Group",
        max_length=20
    )
    # Menu Assigned to each group
    menu = Field.ListField(
        Field.LazyReferenceField('Scope', reverse_delete_rule=PULL),
        help_text="Associated Menu",
        default=list,
        null=True
    )
    # Modified date
    modified_date = Field.DateTimeField(
        help_text="Modified Date Time",
        default=datetime.utcnow()
    )
    meta = {'collection': 'groups'}


# User document for permission informations
class Scope(Document):
    ''' Defines user level security clearance '''
    # Name of the menu to work on e.g. dashboard
    menu = Field.StringField(
        help_text="Available Action Type",
        max_length=20
    )
    # Permission type : space seperated (read/write/update/delete)
    permission = Field.ListField(
        Field.String(max_length=50),
        help_text="Permission Enabled : Space Seperated List",
        default=list,
    )
    # Modified date
    modified_date = Field.DateTimeField(
        help_text="Modification Date Time",
        default=datetime.utcnow()
    )
    meta = {'collection': 'menu'}
