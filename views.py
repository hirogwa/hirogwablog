from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from models import Entry, Blog, Category, Comment
from search import get_query
from datetime import datetime
from django.http import HttpResponseRedirect
import unicodedata


PER_PAGE = 10


def index(request):
    all_entries = Entry.objects.all().order_by('-pub_date')
    return paginated_view(request, all_entries)


def archive(request):
    entries = Entry.objects.all().order_by('-pub_date')
    context = {'entries': entries}
    return render(request, 'blog/archive.html', add_universal_content(context))


# displays multiple entries with pagination
def paginated_view(request, entry_list, html_file='blog/page.html', context={}):
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


# displays single entry with no pagination
def single_entry_view(request, entry_obj, html_file="blog/entry.html", context={}):
    comments = Comment.objects.filter(entry=entry_obj.id).order_by('pub_date')
    context['entries'] = [entry_obj]
    context['comments'] = comments
    return render(request, html_file, add_universal_content(context))


def entry_by_id(request, entry_id):
    blog_entry = get_object_or_404(Entry, pk=entry_id)

    # POST request: comment
    if request.method == 'POST':
        params = request.POST
        new_comment = Comment(entry=blog_entry,
                              author=params.get('author'),
                              email=params.get('email'),
                              content=params.get('content'),
                              pub_date=datetime.now())
        new_comment.save()
        return HttpResponseRedirect("/blog/entry-id/%d" % int(entry_id))

    # otherwise, just a single-entry view
    else:
        return entry(request, blog_entry)


def entry_by_slug(request, slug_text):
    blog_entry = get_object_or_404(Entry, slug=slug_text)
    return entry(request, blog_entry)


def entry(request, blog_entry):
    return single_entry_view(request, blog_entry)


def category(request, category_obj):
    entries = Entry.objects.filter(category=category_obj.id).order_by('-pub_date')
    return paginated_view(request, entries, html_file="blog/category.html", context={"category_string": category_obj})


def category_by_name(request, category_name):
    cat = get_object_or_404(Category, name=category_name)
    return category(request, cat)


def add_universal_content(context):
    context['blog'] = Blog.objects.get(pk=1)
    return add_sidebar_info(context)


def add_sidebar_info(context):
    recent_entries = Entry.objects.order_by('-pub_date')[:10]
    recent_comments = Comment.objects.order_by('-pub_date')[:7]
    categories = Category.objects.all()
    context['categories'] = categories
    context['recent_entries'] = recent_entries
    context['recent_comments'] = recent_comments
    return context


def search(request):
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string_base = request.GET['q']
        query_string = unicodedata.normalize('NFKC', query_string_base)
        entry_query = get_query(query_string, ['title', 'content'])
        found_entries = Entry.objects.filter(entry_query).order_by('-pub_date')
        context = {'query_string': query_string}
        return paginated_view(request, found_entries, html_file='blog/search.html', context=context)
    else:
        return index(request)
