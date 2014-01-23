from django.forms import ModelForm
from bookmarks.models import Bookmark

class BookmarkForm(ModelForm):
    class Meta:
        model = Bookmark
        fields = ['url', 'name', 'personal', 'public']
