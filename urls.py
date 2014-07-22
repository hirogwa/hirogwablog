from django.conf.urls import patterns, url
from entryfeed import LatestEntriesFeed
import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^entry\-by\-id/(?P<entry_id>\d+)/$', views.entry_by_id, name='entry'),
                       url(r'^entry/(?P<slug_text>\S+)/$', views.entry_by_slug, name='entry_by_slug'),
                       url(r'^category/(?P<category_name>\S+)/$', views.category_by_name, name='category_by_name'),
                       url(r'^archive$', views.archive, name='archive'),

                       url(r'^$', LatestEntriesFeed(), name='feed'),
                       )
