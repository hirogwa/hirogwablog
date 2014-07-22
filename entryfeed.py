from django.contrib.syndication.views import Feed
from blog.models import Entry


class LatestEntriesFeed(Feed):
    title = 'hirogwa blog'
    link = '/feed/'
    description = 'When I get sad, I stop being sad and be awesome instead. True story.'

    def items(self):
        return Entry.objects.order_by('-pub_date')[:5]

    def item_title(self, entry):
        return entry.title

    def item_description(self, entry):
        return entry.content
