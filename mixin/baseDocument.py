from mongoengine import Document, CASCADE
from mongoengine import fields as Field
from authentication.models import User
from authentication.serializers import UserOut


class OwnerDocument(Document):
    ''' Base model to provide user information '''

    user = Field.ReferenceField(
        User,
        help_text="User",
        reverse_delete_rule=CASCADE,
        required=True
    )

    @property
    def owner(self):
        user = self.user
        owner = UserOut(username=user.username,
                        id=user.id,
                        first_name=user.first_name,
                        last_name=user.last_name
                        )
        return owner

    meta = {
        'abstract': True,
    }


class TagsDocument(Document):
    ''' Base Model for Tags '''
    # Tags
    tags = Field.ListField(
        Field.StringField(regex="\w",  # noqa : Regex Strig AlphaNumeric
                          max_length=200),
        help_text="tags related to document"
    )

    meta = {
        'abstract': True,
    }


class OwnerAndTags(TagsDocument, OwnerDocument):
    ''' Combination class for owner and tags '''
    meta = {
        'abstract': True,
    }
