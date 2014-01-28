from django.conf.urls import include, patterns, url

from bookmarks import views

urlpatterns = patterns('',
    url(r'^$', views.PersonalIndex.as_view(), name='personal'),
    url(r'^(?P<username>\w+)/$', views.PublicIndex.as_view(), name='public'),
    url(r'^(?P<pk>\d+)/personaldelete/$', views.PersonalDisown.as_view(), name='personal_disown'),
    url(r'^(?P<pk>\d+)/publicdelete/$', views.PublicDisown.as_view(), name='public_disown'),
    url(r'^(?P<pk>\d+)/edit/$', views.EditOwnership.as_view(), name='edit'),
)
