from mongoengine import Document
from mongoengine import fields as Field


class TagsDocument(Document):
    ''' Base Model to be inherited from '''
    # Tags
    tags = Field.ListField(
        Field.StringField(regex="/w",
                          max_length="200"),  # alpha numeric
        help_text="tags related to document"
    )

    meta = {
        'abstract': True,
    }
