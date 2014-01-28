from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from bookmarks.models import Bookmark, Ownership, PersonalOwnership, PublicOwnership
from bookmarks.forms import CreateBookmarkForm, EditOwnershipForm

class Index(CreateView):
    model = Bookmark
    form_class = CreateBookmarkForm

    def form_valid(self, form):
        bookmark = form.save(commit=False)
        bookmark.save()
        user = self.request.user
        name = form.cleaned_data.get('name')
        personal = form.cleaned_data.get('personal')
        public = form.cleaned_data.get('public')
        if personal:
            PersonalOwnership.objects.create(user=user.profile, bookmark=bookmark, name=name)
        if public:
            PublicOwnership.objects.create(user=user.profile, bookmark=bookmark, name=name)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        kwargs['username'] = self.request.user.username
        return super(Index, self).get_context_data(**kwargs)

class PersonalIndex(Index):
    template_name = 'bookmarks/personal_index.html'

    def get_context_data(self, **kwargs):
        profile = self.request.user.profile
        ownership_list = profile.personal_set.all().select_related("bookmark")
        kwargs['latest_ownership_list'] = ownership_list.order_by('-date')
        return super(PersonalIndex, self).get_context_data(**kwargs)

    def get_success_url(self):
        return reverse('personal')

class PublicIndex(Index):
    template_name = 'bookmarks/public_index.html'

    def get_context_data(self, **kwargs):
        profile = self.request.user.profile
        ownership_list = profile.public_set.all().select_related("bookmark")
        kwargs['latest_ownership_list'] = ownership_list.order_by('-date')
        return super(PublicIndex, self).get_context_data(**kwargs)

    def get_success_url(self):
        return reverse('public', kwargs={'username':self.request.user.username})

class EditOwnership(UpdateView):
    model = Ownership
    form_class = EditOwnershipForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse('personal')

class Disown(DeleteView):

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        bookmark = self.object.bookmark
        self.object.delete()
        if not (bookmark.personal_owners.all() or bookmark.public_owners.all()):
            bookmark.delete()
        return HttpResponseRedirect(self.get_success_url())

    def get(self, *args, **kwargs):
        return self.delete(*args, **kwargs)

class PersonalDisown(Disown):
    model = PersonalOwnership

#    def get(self, *args, **kwargs):
#        return self.delete(*args, **kwargs)

    def get_success_url(self):
        return reverse('personal')

class PublicDisown(Disown):
    model = PublicOwnership

    def get_success_url(self):
        return reverse('public', kwargs={'username':self.request.user.username})
