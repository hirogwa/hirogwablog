from blog.models import Blog, Entry, Comment
from bs4 import BeautifulSoup
from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404


class LatestEntriesFeed(Feed):
    blog_obj = get_object_or_404(Blog, pk=1)
    title = blog_obj.name
    link = '/blog/feed/'
    description = blog_obj.description

    def items(self):
        return Entry.objects.order_by('-pub_date')[:5]

    def item_title(self, entry):
        return entry.title

    def item_pubdate(self, entry):
        return entry.pub_date

    def item_description(self, entry):
        parsed = BeautifulSoup(entry.content)
        return '%s [...]' % parsed.p


class RecentCommentsFeed(Feed):
    blog_obj = get_object_or_404(Blog, pk=1)
    title = 'Comments on %s' % blog_obj.name
    link = '/blog/feed/comments'
    description = blog_obj.description

    def items(self):
        return Comment.objects.order_by('-pub_date')[:5]

    def item_title(self, comment):
        return '%s on %s' % (comment.author, comment.entry.title)

    def item_pubdate(self, comment):
        return comment.pub_date

    def item_description(self, comment):
        return comment.content
