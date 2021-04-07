from mongoengine import Document, CASCADE
from mongoengine import fields as Field
from authentication.models import User
from items.models import Product
from places.models import Place
from datetime import datetime


# Ratings document for rating information
class Ratings(Document):
    thread = Field.GenericReferenceField(
        help_text="Generic Reference to all the modules",
        required=True
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
        User,
        help_text="User",
        reverse_delete_rule=CASCADE
    )


# Ratings document for Comment information
class Comments(Document):
    thread = Field.GenericReferenceField(
        help_text="Generic Reference to all the modules",
        required=True,
        choices=[Place, Product]
    )
    comment = Field.StringField(
        help_text="User rating",
        default=0,
        required=True
    )
    user = Field.ReferenceField(
        User,
        help_text="User",
        reverse_delete_rule=CASCADE
    )
    modified_date = Field.DateTimeField(
        help_text="Modified Date",
        default=datetime.utcnow()
    )
