from django.db import models
from django.template.defaultfilters import slugify


class Blog(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

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
        self.slug = '%i%02d%02d%02d%02d-%s' % (
            date.year, date.month, date.day, date.hour, date.minute, slugify(self.title)
        )
        super(Entry, self).save()
