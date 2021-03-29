from mongoengine import DynamicDocument
from mongoengine import fields as Field


# User document for Product informations.
# Dynamic Document is used to store incomming relevant details if any
class Place(DynamicDocument):
    ''' Product Description
        Additional Details:
            Manufacture and Expiry Date
            Tags
            Related products
            Supplied By, Manufacturer
            Ships From and Shipping Costs
    '''
    # Unique Id for the current Item
    product_Id = Field.SequenceField(
        db_field="Id",
        help_text="Product Id",
        required=True,
        primary_key=True
    )
    # Name for the current Item
    product_name = Field.StringField(
        db_field="name",
        help_text="Product Name",
        required=True,
        max_length=50
    )
    # Type for the current Item
    product_type = Field.StringField(
        db_field="type",
        help_text="Product Type : Food / Decoration / Colors etc",
        null=True,
        max_length=50
    )
    # Product Description
    product_desc = Field.StringField(
        db_field="description",
        help_text="Product Description",
        max_length="2000"
    )
    # Listed Price
    price = Field.DecimalField(
        help_text="Per Unit Price",
        default=0.00
    )
