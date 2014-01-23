from django.conf.urls import patterns, url

from bookmarks import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/delete/$', views.DeleteBookmark.as_view(), name='delete'),
    url(r'^(?P<pk>\d+)/edit/$', views.EditBookmarkView.as_view(), name='edit'),
)
