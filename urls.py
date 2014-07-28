from django.conf.urls import patterns, url
from feed import LatestEntriesFeed, RecentCommentsFeed
import api
import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),

                       # entry single view.
                       url(r'^entry/(?P<slug_text>\S+)/$', views.entry_by_slug, name='entry_by_slug'),
                       url(r'^entry-id/(?P<entry_id>\d+)/$', views.entry_by_id, name='entry'),

                       url(r'^category/(?P<category_name>\S+)/$', views.category_by_name, name='category_by_name'),
                       url(r'^archive/$', views.archive, name='archive'),
                       url(r'^search/$', views.search, name='search'),

                       # feed
                       url(r'^feed/$', LatestEntriesFeed(), name='feed'),
                       url(r'^feed/comment/$', RecentCommentsFeed(), name='feed_comments'),

                       # api
                       url(r'^api/entry/list/$', api.entry_list),
                       url(r'^api/entry/list/(?P<keyword>\S+)/$', api.entry_list_filter),
                       url(r'^api/entry/new/$', api.entry_new),
                       url(r'^api/entry/$', api.entry_push),
                       url(r'^api/entry/(?P<entry_id>\d+)/$', api.entry),
                       )
