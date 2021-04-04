from mongoengine import Document
from mongoengine import fields as Field
from authentication.models import User  # noqa E501
from items.models import Product  # noqa E501
from places.models import Place   # noqa E501
from datetime import datetime


# Ratings document for rating information
class Ratings(Document):
    thread = Field.GenericLazyReferenceField(
        help_text="Generic Reference to all the modules",
        choices=['Place', 'Product']
    )
    rating = Field.DecimalField(
        help_text="User rating",
        default=0
    )
    review = Field.StringField(
        help_text="User Review",
        default=0,
        required=True
    )
    user = Field.ReferenceField(
        'User',
        help_text="User",
        required=True
    )


# Ratings document for Comment information
class Comments(Document):
    thread = Field.GenericLazyReferenceField(
        help_text="Generic Reference to all the modules",
        choices=['Place', 'Product']
    )
    comment = Field.StringField(
        help_text="User rating",
        default=0,
        required=True
    )
    user = Field.ReferenceField(
        'User',
        help_text="User",
        required=True
    )
    modified_date = Field.DateTimeField(
        help_text="Modified Date",
        default=datetime.utcnow()
    )
