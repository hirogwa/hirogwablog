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

    def __unicode__(self):
        return self.title

    def save(self):
        date = datetime.date.today()
        self.slug = '%i%i%i-%s' % (
            date.year, date.month, date.day, slugify(self.title)
        )
        super(Entry, self).save()

