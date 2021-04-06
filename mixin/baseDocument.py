from mongoengine import Document
from mongoengine import fields as Field


class TagsDocument(Document):
    ''' Base Model to be inherited from '''
    # Tags
    tags = Field.ListField(
        Field.StringField(regex="\w",  # noqa : Regex Strig AlphaNumeric
                          max_length=200),
        help_text="tags related to document"
    )

    meta = {
        'abstract': True,
    }
