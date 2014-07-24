from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from models import Entry, Blog, Category
from search import get_query


PER_PAGE = 10


def index(request):
    return unfiltered(request)


def archive(request):
    entries = Entry.objects.all().order_by('-pub_date')
    context = {'entries': entries}
    return render(request, 'blog/archive.html', add_universal_content(context))


def page(request, entry_list, html_file='blog/page.html', context={}):

    paginator = Paginator(entry_list, PER_PAGE)
    page_number = request.GET.get('page')
    try:
        entries = paginator.page(page_number)
    except PageNotAnInteger:
        entries = paginator.page(1)
    except EmptyPage:
        entries = paginator.page(paginator.num_pages)
    context['entries'] = entries
    context['host'] = request.META['HTTP_HOST']
    return render(request, html_file, add_universal_content(context))


def unfiltered(request):
    all_entries = Entry.objects.all().order_by('-pub_date')
    return page(request, all_entries)


def entry_by_id(request, entry_id):
    blog_entry = get_object_or_404(Entry, pk=entry_id)
    return entry(request, blog_entry)


def entry_by_slug(request, slug_text):
    blog_entry = get_object_or_404(Entry, slug=slug_text)
    return entry(request, blog_entry)


def entry(request, blog_entry):
    entries = [blog_entry]
    return page(request, entries)


def category(request, category_obj):
    entries = Entry.objects.filter(category=category_obj.id).order_by('-pub_date')
    return page(request, entries, html_file="blog/category.html", context={"category_string": category_obj})


def category_by_name(request, category_name):
    cat = get_object_or_404(Category, name=category_name)
    return category(request, cat)


def add_universal_content(context):
    context['blog'] = Blog.objects.get(pk=1)
    return add_sidebar_info(context)


def add_sidebar_info(context):
    recent_entries = Entry.objects.order_by('-pub_date')[:10]
    categories = Category.objects.all()
    context['categories'] = categories
    context['all_entries'] = recent_entries
    return context


def search(request):
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = get_query(query_string, ['title', 'content'])
        found_entries = Entry.objects.filter(entry_query).order_by('-pub_date')
        context = {'query_string': query_string}
        return page(request, found_entries, html_file='blog/search.html', context=context)
    else:
        return index(request)
