from mixin.baseDocument import TagsDocument
from mongoengine import fields as Field
from authentication.models import User  # noqa E501


# Place document for Place informations.
class Place(TagsDocument):
    ''' Place Description
        Additional Details:
            Tags    : Store Tags for place
            Ratings : Store User Ratings
    '''
    # Name for the Place
    name = Field.StringField(
        help_text="Place Name",
        required=True,
        max_length=50
    )
    # Type for the current Place
    category = Field.StringField(
        help_text="Place Type : Natural / Dine in / Hisotircal etc",
        max_length=50
    )
    # Type for the current Item
    country = Field.StringField(
        help_text="Country",
        max_length=50
    )
    # Type for the current Item
    city = Field.StringField(
        help_text="City",
        max_length=50
    )

    location = Field.GeoPointField(
        help_text="Latitude and Logitude of place"
    )
    # Place Description
    description = Field.StringField(
        help_text="Description for place",
        max_length="2000"
    )
    owner = Field.ReferenceField(
        'User',
        help_text="User",
        required=True
    )
