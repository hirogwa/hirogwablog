from django.db import models
from django.template.defaultfilters import slugify
import urllib, hashlib


class Blog(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    facebook_app_id = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name


class Category(models.Model):
    blog = models.ForeignKey(Blog)
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Entry(models.Model):
    blog = models.ForeignKey(Blog)
    category = models.ForeignKey(Category)
    title = models.TextField()
    content = models.TextField()
    slug = models.SlugField()
    pub_date = models.DateTimeField('published_time')

    def spaced_date(self):
        return '%d %02d %02d' % \
            (self.pub_date.year, self.pub_date.month, self.pub_date.day)

    def get_absolute_url(self):
        return '/blog/entry/%s' % self.slug

    def __unicode__(self):
        return self.title

    def save(self):
        date = self.pub_date
        if self.slug == '':
            slug_base = self.title
        else:
            slug_base = self.slug

        self.slug = '%i%02d%02d-%s' % (date.year, date.month, date.day, slugify(slug_base))
        super(Entry, self).save()


class Comment(models.Model):
    entry = models.ForeignKey(Entry)
    author = models.CharField(max_length=60)
    email = models.EmailField()
    content = models.TextField()
    pub_date = models.DateTimeField('published_time')

    def anchor_id(self):
        date = self.pub_date
        return '%s-%d%02d%02d%02d%02d' % \
            (self.author, date.year, date.month, date.day, date.hour, date.minute)

    def pub_date_string(self):
        date = self.pub_date
        return '%d %02d %02d %02d:%02d' % \
               (date.year, date.month, date.day, date.hour, date.minute)

    def __unicode__(self):
        date = self.pub_date
        return '%i%02d%02d%02d%02d-%s-%s' % (
            date.year, date.month, date.day, date.hour, date.minute, self.author, self.entry.title)

    def gravatar_url(self):
        size = 60
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(self.email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'s': str(size)})
        return gravatar_url

    def get_absolute_url(self):
        return '/blog/entry-id/%d/#%s' % (self.entry.id, self.anchor_id())
