#!/usr/bin/python
# -*- coding: utf-8 -*-
if __name__ in ("escontrol", "__main__"):
    '''
    add project settings to path when called outside the django app.
    '''
    import os
    import sys
    import yaml
    configfile = file('blog.yaml', 'r')
    config = yaml.load(configfile)
    sys.path.append(config.get('project_directory'))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', config.get('project_settings'))

from django.utils.html import strip_tags
from elasticsearch import Elasticsearch
import models
import essettings


class ESControl():
    def __init__(self, index=None, doc_type=None):
        b = models.Blog.objects.all()[0]
        self._index = index or b.elastic_search_index
        self._doc_type = doc_type or b.elastic_search_doc_type
        self._es = Elasticsearch()

    @staticmethod
    def _hit_item_element(hit_item, element, fill_source=True):
        highlight = hit_item.get('highlight')
        source = hit_item.get('_source')
        if highlight and highlight.get(element):
            return '...'.join(highlight.get(element))
        elif fill_source:
            return source.get(element)
        else:
            return ''

    def remove_entry(self, entry):
        self._es.delete(index=self._index, doc_type=self._doc_type, id=entry.id)

    def import_entry(self, entry):
        doc = {'title': entry.title,
               'slug': entry.slug,
               'content': strip_tags(entry.content),
               'category': entry.category.name,
               'pub_date': entry.pub_date}
        self._es.index(index=self._index, doc_type=self._doc_type, id=entry.id, body=doc)

    def import_entries(self):
        entries = models.Entry.objects.all()
        for entry in entries:
            self.import_entry(entry)

    def delete_index(self):
        self._es.indices.delete(self._index)

    def create_index(self):
        self._es.indices.create(self._index, essettings.index_definition(self._doc_type))

    def update_analyzer_kuromoji(self):
        self._es.indices.close(self._index)
        self._es.indices.put_settings(essettings.kuromoji_analyzer_def(), self._index)
        self._es.indices.open(self._index)

    def search_entries(self, query):
        hits = self._es.search(index=self._index,
                               doc_type=self._doc_type,
                               body=essettings.search_query_body(query))['hits']
        hit_list = []
        for hit in hits['hits']:
            item = {
                'score': hit.get('_score'),
                'title': self._hit_item_element(hit, 'title'),
                'slug': self._hit_item_element(hit, 'slug'),
                'slug_source': hit.get('_source').get('slug'),
                'content': self._hit_item_element(hit, 'content', fill_source=False),
                'category': self._hit_item_element(hit, 'category'),
                'pub_date': self._hit_item_element(hit, 'pub_date'),
            }
            hit_list.append(item)
        return hit_list

if __name__ == '__main__':
    '''
    set up elasticsearch, assuming Japanese entries.
    '''
    blog_list = models.Blog.objects.all()
    if blog_list:
        b = blog_list[0]
        if b.elastic_search_index and b.elastic_search_doc_type:
            es = ESControl(b.elastic_search_index, b.elastic_search_doc_type)
            es.create_index()
            es.import_entries()
            es.update_analyzer_kuromoji()
        else:
            print ('Blog.elastic_search_index and Blog.elastic_search_doc_type not defined.')
    else:
        print ('no blog found')

