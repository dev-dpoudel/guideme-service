from mongoengine import fields as Field
from mixin.baseDocument import TagsDocument


# User document for Product informations.
# Dynamic Document is used to store incomming relevant details if any
class Product(TagsDocument):
    ''' Product Description
        Additional Details:
            Manufacture and Expiry Date
            Tags
            Related products
            Supplied By, Manufacturer
            Ships From and Shipping Costs
    '''
    # Name for the current Item
    name = Field.StringField(
        db_field="name",
        help_text="Product Name",
        required=True,
        max_length=50
    )
    # Unique Id for the current Item
    identity = Field.StringField(
        db_field="identity",
        help_text="Product Id"
    )
    # Type for the current Item
    type = Field.StringField(
        db_field="type",
        help_text="Product Type : Food / Decoration / Colors etc",
        max_length=50
    )
    # Product Description
    description = Field.StringField(
        db_field="description",
        help_text="Product Description",
        max_length="2000"
    )
    # Listed Price
    price = Field.DecimalField(
        help_text="Per Unit Price",
    )
    # Status
    available = Field.BooleanField(
        help_text="Availability of Items",
        default=True
    )
    # Manufacture Date
    manufacture_date = Field.DateTimeField(
        help_text="Date Time of Manufacture",
        null=False
    )
    # Expiration Date
    expiry_date = Field.DateTimeField(
        help_text="Expiry",
        null=False
    )
