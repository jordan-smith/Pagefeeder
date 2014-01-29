from django.test import TestCase, Client
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import timezone

from bookmarks.models import Bookmark, PersonalOwnership, PublicOwnership
from bookmarks.views import PersonalIndex, PublicIndex 
from users.models import UserProfile

def create_personal_bookmark(userprofile, url="http://www.reddit.com", name="reddit"):
    bookmark = Bookmark.objects.create(url=url)
    return PersonalOwnership.objects.create(user=userprofile, bookmark=bookmark, name=name)

def create_public_bookmark(userprofile, url="http://www.reddit.com", name="reddit"):
    bookmark = Bookmark.objects.create(url=url)
    return PublicOwnership.objects.create(user=userprofile, bookmark=bookmark, name=name)

def create_personalpublic_bookmark(userprofile, url="http://www.reddit.com", name="reddit"):
    bookmark = Bookmark.objects.create(url=url)
    PersonalOwnership.objects.create(user=userprofile, bookmark=bookmark, name=name)
    PublicOwnership.objects.create(user=userprofile, bookmark=bookmark, name=name)
    return bookmark

class BookmarkTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('username', 'test@gmail.com', 'password')
        UserProfile.objects.create(user=self.user)

    def test_is_orphan(self):
        """
        If a bookmark has any public/private ownership relationships, is_orphan should
        return true. Otherwise is_orphan should return false.
        """
        bookmark = create_personalpublic_bookmark(userprofile=self.user.profile)
        self.assertFalse(bookmark.is_orphan())
        bookmark.personal_set.all().delete()        
        self.assertFalse(bookmark.is_orphan())
        bookmark.public_set.all().delete()        
        self.assertTrue(bookmark.is_orphan())

class IndexTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user('username', 'test@gmail.com', 'password')
        UserProfile.objects.create(user=self.user)

    def test_no_bookmarks(self):
        """
        If no bookmarks exist, an appropriate message should be displayed in
        both the personal and public index views.
        """
#        request = self.factory.get(reverse('personal'))
#        request.user = self.user
#        response = PersonalIndex.as_view()(request)
#        self.assertEqual(response.status_code, 200)
#        self.assertContains(response, "No pages are bookmarked.")
#        self.assertQuerysetEqual(response.context['latest_ownership_list'], [])

        logged_in = self.client.login(username='username', password='password')
        self.assertTrue(logged_in)
        response = self.client.get(reverse('personal'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No pages are bookmarked.")
        self.assertQuerysetEqual(response.context['latest_ownership_list'], [])

        response = self.client.get(reverse('public', kwargs={'username':self.user.username}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No pages are bookmarked.")
        self.assertQuerysetEqual(response.context['latest_ownership_list'], [])

    def test_with_a_personal_bookmark(self):
        """
        personal bookmarks should appear in the personal index, and not
        in the public index
        """
        logged_in = self.client.login(username='username', password='password')
        self.assertTrue(logged_in)
        create_personal_bookmark(userprofile=self.user.profile)
        response = self.client.get(reverse('personal'))
        self.assertQuerysetEqual(response.context['latest_ownership_list'], ['<PersonalOwnership: reddit>'])

        response = self.client.get(reverse('public', kwargs={'username':self.user.username}))
        self.assertQuerysetEqual(response.context['latest_ownership_list'], [])

    def test_with_a_public_bookmark(self):
        """
        public bookmarks should not appear in the public index, and not
        in the personal index
        """
        logged_in = self.client.login(username='username', password='password')
        self.assertTrue(logged_in)
        create_public_bookmark(userprofile=self.user.profile)
        response = self.client.get(reverse('personal'))
        self.assertQuerysetEqual(response.context['latest_ownership_list'], [])

        response = self.client.get(reverse('public', kwargs={'username':self.user.username}))
        self.assertQuerysetEqual(response.context['latest_ownership_list'], ['<PublicOwnership: reddit>'])

    def test_personal_with_a_personalpublic_bookmark(self):
        """
        bookmarks that are both personal and public should appear in both
        the personal and public indexes
        """
        logged_in = self.client.login(username='username', password='password')
        self.assertTrue(logged_in)
        create_personalpublic_bookmark(userprofile=self.user.profile)
        response = self.client.get(reverse('personal'))
        self.assertQuerysetEqual(response.context['latest_ownership_list'], ['<PersonalOwnership: reddit>'])

        response = self.client.get(reverse('public', kwargs={'username':self.user.username}))
        self.assertQuerysetEqual(response.context['latest_ownership_list'], ['<PublicOwnership: reddit>'])
