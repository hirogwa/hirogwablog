import os
import sys
sys.path.append('/Users/hirogwa/Documents/workspace/sitehirogwa')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sitehirogwa.settings')

from django.utils.html import strip_tags
from elasticsearch import Elasticsearch
from models import Entry


class ESControl():
    def __init__(self):
        self._index = 'hirogwa_blog'
        self._type = 'blog_entry'
        self._es = Elasticsearch()

    def import_entries(self):
        entries = Entry.objects.all()
        for entry in entries:
            doc = {'title': entry.title,
                   'slug': entry.slug,
                   'content': strip_tags(entry.content),
                   'category': entry.category.name,
                   'pub_date': entry.pub_date}
            self._es.index(index=self._index, doc_type=self._type, id=entry.id, body=doc)

    @staticmethod
    def _hit_item_element(hit_item, element, fill_source=True):
        highlight = hit_item.get('highlight')
        source = hit_item.get('_source')
        if highlight.get(element):
            return '...'.join(highlight.get(element))
        elif fill_source:
            return source.get(element)
        else:
            return ''

    def search_entries(self, query):
        query_body = {
            'query': {
                'multi_match': {
                    'query': query,
                    'fields': ['title', 'slug', 'content', 'category']
                }
            },
            'highlight': {
                'fields': {
                    'title': {},
                    'slug': {},
                    'content': {},
                    'category': {},
                }
            }
        }
        hits = self._es.search(index=self._index, doc_type=self._type, body=query_body)['hits']

        hit_list = []
        for hit in hits['hits']:
            item = {
                'score': hit.get('_score'),
                'title': self._hit_item_element(hit, 'title'),
                'slug': self._hit_item_element(hit, 'slug'),
                'content': self._hit_item_element(hit, 'content', fill_source=False),
                'category': self._hit_item_element(hit, 'category'),
                'pub_date': self._hit_item_element(hit, 'pub_date'),
            }
            hit_list.append(item)
        return hit_list

if __name__ == '__main__':
    esc = ESControl()
    esc.import_entries()
