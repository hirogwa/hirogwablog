from django.shortcuts import render, get_object_or_404
from models import Entry, Blog, Category


def index(request):
    blog = Blog.objects.get(pk=1)
    latest_entries = Entry.objects.order_by('-pub_date')[:10]
    context = {'blog': blog,
               'entries': latest_entries}
    return render(request, 'blog/index.html', add_sidebar_info(context))


def entry_by_id(request, entry_id):
    blog_entry = get_object_or_404(Entry, pk=entry_id)
    return entry(request, blog_entry)


def entry_by_slug(request, slug_text):
    blog_entry = get_object_or_404(Entry, slug=slug_text)
    return entry(request, blog_entry)


def entry(request, blog_entry):
    entries = [blog_entry]
    context = {'entries': entries, 'blog': blog_entry.blog}
    return render(request, 'blog/entry.html', add_sidebar_info(context))


def category(request, category_obj):
    entries = Entry.objects.filter(category=category_obj.id).order_by('-pub_date')
    context = {'entries': entries, 'blog': category_obj.blog}
    return render(request, 'blog/category.html', add_sidebar_info(context))


def category_by_name(request, category_name):
    cat = get_object_or_404(Category, name=category_name)
    return category(request, cat)


def add_sidebar_info(context):
    all_entries = Entry.objects.order_by('-pub_date')
    categories = Category.objects.all()
    context['categories'] = categories
    context['all_entries'] = all_entries
    return context
