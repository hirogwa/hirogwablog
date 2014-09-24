"""
responsible for talking to disqus to satisfy any disqus related needs.
"""
import json
import os
import urllib2
import yaml


class Disqus:
    def __init__(self):
        configfile = file(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'blog.yaml'), 'r')
        config = yaml.load(configfile)
        self._api_key = config.get('api_key')
        self._api_secret = config.get('api_secret')
        self._access_token = config.get('access_token')

    def _request_get(self, url, api_key=True, api_secret=True, **kwargs):
        url += '?access_token=' + self._access_token
        if api_key:
            kwargs['api_key'] = self._api_key
        if api_secret:
            kwargs['api_secret'] = self._api_secret
        for k, v in kwargs.items():
            url += '&' + k + '=' + str(v)
        return urllib2.urlopen(url).read()

    def _thread(self, thread_id):
        url = 'https://disqus.com/api/3.0/threads/details.json'
        return json.loads(self._request_get(url, thread=thread_id))

    def get_post_list(self, forum, **kwargs):
        """
        returns the list of comments associated with the given forum.
        :param forum:
        :param kwargs:
        :return:
        """
        url = 'https://disqus.com/api/3.0/forums/listPosts.json'
        response_list = json.loads(self._request_get(url, forum=forum, **kwargs))['response']
        comment_list = []
        for r in response_list:
            comment_list.append({'author': r['author']['name'].encode('utf-8'),
                                 'content': r['raw_message'].encode('utf-8'),
                                 'pub_date': r['createdAt'].encode('utf-8'),
                                 })
        return comment_list
