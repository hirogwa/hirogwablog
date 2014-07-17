from django.shortcuts import render, get_object_or_404
from models import Entry, Blog


def index(request):
    blog = Blog.objects.get(pk=1)
    latest_entries = Entry.objects.all()
    context = {'latest_entries': latest_entries, 'blog': blog}
    return render(request, 'blog/index.html', context)


def entry_by_id(request, entry_id):
    blog_entry = get_object_or_404(Entry, pk=entry_id)
    return entry(request, blog_entry)


def entry_by_slug(request, slug_text):
    blog_entry = get_object_or_404(Entry, slug=slug_text)
    return entry(request, blog_entry)


def entry(request, blog_entry):
    context = {'entry': blog_entry}
    return render(request, 'blog/entry.html', context)
