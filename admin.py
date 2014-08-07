from django.contrib import admin
from models import Entry, Blog, Category, Comment, Theme, Tag

# Register your models here.
admin.site.register(Blog)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Entry)
admin.site.register(Tag)
admin.site.register(Theme)
