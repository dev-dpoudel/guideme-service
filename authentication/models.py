from mongoengine import Document
from mongoengine import fields as Field
from mongoengine import PULL
from datetime import datetime


# User document for permission informations
class Group(Document):
    ''' Defines User Group for Operations'''
    # Name of the group
    name = Field.StringField(
        help_text="Name of the Group",
        unique=True,
        max_length=20
    )
    # permissions Assigned to each group
    permission = Field.DictField(
        help_text="Associated Permission",
        null=True
    )
    # Modified date
    modified_date = Field.DateTimeField(
        help_text="Modified Date Time",
        default=datetime.utcnow()
    )
    meta = {'collection': 'groups'}


# User document for login informations
class User(Document):
    # Username for the current user
    username = Field.StringField(
        help_text="Unique Username",
        required=True,
        unique=True,
        max_length=20,
        db_field="username"
    )

    # Password for the username
    password = Field.StringField(
        help_text="Password : Hashed",
        required=True,
    )

    # User Profile Image
    profile = Field.ImageField(
        help_text="Profile Image"
    )

    # User associated groups
    group = Field.ListField(
        Field.LazyReferenceField('Group', reverse_delete_rule=PULL),
        help_text="Assigned User Groups",
        null=False
    )

    # Username for the user
    first_name = Field.StringField(
        db_field="first_name",
        help_text="First Name of the user",
        max_length=50,
    )
    # Surname of the user
    last_name = Field.StringField(
        db_field="last_name",
        help_text="Last Name of the User",
        max_length=50,
    )
    # Prefered Name of user
    prefered_name = Field.StringField(
        db_field="prefered_name",
        help_text="Prefered Name of the user",
        max_length=20
    )
    # Birthdate
    birth_date = Field.DateTimeField(
        db_field="birth_date",
        help_text="Birthdate of the User"
    )
    # Nationality
    country = Field.StringField(
        help_text="Country",
        max_length=30
    )
    # City
    city = Field.StringField(
        help_text="City",
        max_length=30
    )
    # Postal/Zip Code
    zip = Field.StringField(
        help_text="Zip Code",
        max_length=8
    )
    # Current Address
    address = Field.StringField(
        help_text="Contact Address",
        max_length=100
    )
    # Permanent Address
    permanent_address = Field.StringField(
        db_field="perm_address",
        help_text="Permanent Address",
        max_length=100
    )
    # User status
    is_active = Field.BooleanField(
        db_field="is_active",
        help_text="Is User Active",
        defult=True
    )
    # Account Email Address
    email_address = Field.EmailField(
        db_field="email_address",
        help_text="User Email Address"
    )
    # Registered Date
    modified_date = Field.DateTimeField(
        db_field="modified_date",
        help_text="Last Modification Date",
        default=datetime.utcnow()
    )

    @property
    def scopes(self):
        scopes = {}
        groups = []
        for group in self.group:
            instance = group.fetch()
            groups.append(instance.name)
            scopes.update(instance.permission.items())
        return groups, scopes

    meta = {'collection': 'users'}
