from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.core.urlresolvers import reverse

from bookmarks.models import Bookmark
from bookmarks.forms import BookmarkForm

class IndexView(CreateView):
    form_class = BookmarkForm
    template_name = 'bookmarks/index.html'

    def get_success_url(self):
        return reverse('index')

    def get_context_data(self, **kwargs):
        kwargs['latest_bookmark_list'] = Bookmark.objects.order_by('-mark_date')
        return super(IndexView, self).get_context_data(**kwargs)

class DeleteBookmark(DeleteView):
    model = Bookmark

    def get_success_url(self):
        return reverse('index')

    def get(self, *args, **kwargs):
        return self.delete(*args, **kwargs)

class EditBookmarkView(UpdateView):
    model = Bookmark
    form_class = BookmarkForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse('index')
