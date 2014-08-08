from django.db import models
from django.template.defaultfilters import slugify
import urllib
import hashlib


class Theme(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=400)
    css_file = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Blog(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    facebook_app_id = models.CharField(max_length=30)
    theme = models.ForeignKey(Theme)
    author_email = models.EmailField()

    def __unicode__(self):
        return self.name

    def gravatar_url(self):
        return gravatar_url(self.author_email, 150)


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

    def tags(self):
        return Tag.objects.filter(entry=self.id)

    def spaced_datetime(self):
        return '%d %02d %02d %02d:%02d' % \
               (self.pub_date.year, self.pub_date.month, self.pub_date.day, self.pub_date.hour, self.pub_date.minute)

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
            self.slug = '%i%02d%02d-%s' % (date.year, date.month, date.day, slugify(slug_base))
        super(Entry, self).save()


class Tag(models.Model):
    name = models.CharField(max_length=100)
    entry = models.ForeignKey(Entry, db_index=True)

    def __unicode__(self):
        return '%s,%s' % (self.name, self.entry.title)


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
        return gravatar_url(self.email, 60)

    def get_absolute_url(self):
        return '/blog/entry-id/%d/#%s' % (self.entry.id, self.anchor_id())


def gravatar_url(email, size):
    url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
    url += urllib.urlencode({'s': str(size)})
    return url
