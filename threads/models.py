from mongoengine import fields as Field
from items.models import Product
from places.models import Place
from datetime import datetime
from mixin.baseDocument import OwnerDocument


# Ratings document for rating information
class Ratings(OwnerDocument):
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


# Ratings document for Comment information
class Comments(OwnerDocument):
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
    modified_date = Field.DateTimeField(
        help_text="Modified Date",
        default=datetime.utcnow()
    )
