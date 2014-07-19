import datetime
from django.db import models
from django.template.defaultfilters import slugify


class Blog(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()


class Entry(models.Model):
    blog = models.ForeignKey(Blog)
    title = models.TextField()
    content = models.TextField()
    slug = models.SlugField()
    pub_date = models.DateTimeField('published_time')

    def spaced_date(self):
        return '%d %02d %02d' % \
            (self.pub_date.year, self.pub_date.month, self.pub_date.day)

    def __unicode__(self):
        return self.title

    def save(self):
        now = datetime.datetime.now()
        self.slug = '%i%02d%02d%02d%02d-%s' % (
            now.year, now.month, now.day, now.hour, now.minute, slugify(self.title)
        )
        super(Entry, self).save()

