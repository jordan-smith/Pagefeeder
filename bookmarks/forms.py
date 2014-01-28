from django.forms import ValidationError, ModelForm, CharField, BooleanField
from bookmarks.models import Bookmark, Ownership

class BookmarkForm(ModelForm):
    personal = BooleanField(required=False)
    public = BooleanField(required=False)

    def clean(self):
        cleaned_data = super(BookmarkForm, self).clean()
        personal =  cleaned_data.get("personal")
        public = cleaned_data.get("public")
        if not (personal or public):
            raise ValidationError("You must specify personal/public")
        return cleaned_data


class CreateBookmarkForm(BookmarkForm):
    name = CharField(max_length=100)

    class Meta:
        model = Bookmark
        fields = ['url',]

class EditOwnershipForm(ModelForm):
    class Meta:
        model = Ownership
        fields = ['name',]
