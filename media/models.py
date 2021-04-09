from mongoengine import fields as Field
from items.models import Product
from places.models import Place
from threads.models import Comments, Ratings
from mixin.baseDocument import OwnerDocument


# Ratings document for rating information
class Media(OwnerDocument):
    thread = Field.GenericReferenceField(
        help_text="Generic Reference to all the modules",
        required=True,
        choices=[Place, Product, Ratings, Comments]
    )
    filename = Field.StringField(
        help_text="File Name",
        unique=True
    )
    content = Field.StringField(
        help_text="Content Type",
        required=True
    )
    context = Field.StringField(
        help_text="Associated Type",
        required=True
    )
