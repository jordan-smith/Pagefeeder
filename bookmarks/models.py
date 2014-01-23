from django.db import models
from django.forms import ModelForm
from annoying.fields import AutoOneToOneField

from django.utils import timezone

class Bookmark(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    mark_date = models.DateTimeField(default=timezone.now)
    push_date = models.DateTimeField(blank=True, null=True)
    personal = models.BooleanField(default=True)
    public = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class UserProfile(models.Model):
    user = AutoOneToOneField('auth.user')
    follows = models.ManyToManyField('UserProfile', related_name='followed_by')

    def __unicode(self):
        return self.user.username
