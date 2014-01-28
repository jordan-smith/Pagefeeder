from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from users.models import UserProfile

class Bookmark(models.Model):
    url = models.URLField()

    def __unicode__(self):
        return self.url

class Ownership(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

class PersonalOwnership(Ownership):
    bookmark = models.ForeignKey(Bookmark, related_name="personal_set")
    user = models.ForeignKey(UserProfile, related_name="personal_set")

class PublicOwnership(Ownership):
    bookmark = models.ForeignKey(Bookmark, related_name="public_set")
    user = models.ForeignKey(UserProfile, related_name="public_set")
