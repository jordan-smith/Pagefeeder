from django.db import models
from django.contrib.auth.models import User
from registration.signals import user_registered

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile")
    personal_marks = models.ManyToManyField('bookmarks.Bookmark', 
                            through='bookmarks.PersonalOwnership',
                            related_name='personal_owners'
                            )
    public_marks = models.ManyToManyField('bookmarks.Bookmark', 
                            through='bookmarks.PublicOwnership',
                            related_name='public_owners'
                            )
    follows = models.ManyToManyField('UserProfile',
                            related_name='followed_by',
                            symmetrical=False
                            )
    
    def __unicode__(self):
        return self.user.username    

def user_registered_callback(sender, user, request, **kwargs):
    profile = UserProfile(user=user)
    profile.save()

user_registered.connect(user_registered_callback)
