from django.contrib import admin
from models import Entry, Blog, Category

# Register your models here.
admin.site.register(Blog)
admin.site.register(Entry)
admin.site.register(Category)
