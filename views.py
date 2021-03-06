from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from models import Entry, Blog, Category, Comment, Tag, TagMap
from search import get_query
from datetime import datetime
from django.http import HttpResponseRedirect, Http404
import escontrol
import unicodedata


PER_PAGE = 10


def index(request):
    all_entries = Entry.objects.all().order_by('-pub_date')
    return paginated_view(request, all_entries)


def archive(request):
    entries = Entry.objects.all().order_by('-pub_date')
    context = {'entries': entries}
    context.update(add_universal_content(request))
    return render(request, 'blog/archive.html', context)


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
    context.update(add_universal_content(request))
    return render(request, html_file, context)


# displays single entry with no pagination
def single_entry_view(request, entry_obj, html_file="blog/entry.html", context={}):
    comments = Comment.objects.filter(entry=entry_obj.id).order_by('pub_date')
    context['entries'] = [entry_obj]
    context['similar_entries'] = entry_obj.similar_entries(5)
    context['comments'] = comments
    context.update(add_universal_content(request))
    return render(request, html_file, context)


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


def tag(request, tag_name):
    tag = Tag.objects.get(name=tag_name)
    tag_map = TagMap.objects.filter(tag=tag)
    entry_ids = []
    for pair in tag_map:
        entry_ids.append(pair.entry.id)
    entries = Entry.objects.filter(pk__in=entry_ids).order_by('-pub_date')
    return paginated_view(request, entries, html_file="blog/tag.html", context={"tag_name": tag_name})


def add_universal_content(request):
    blog_obj = Blog.objects.get(pk=1)
    context = {'blog': blog_obj,
               'host': request.META['HTTP_HOST']}
    context.update(add_sidebar_info(blog_obj))
    return context


def add_sidebar_info(blog):
    recent_entries = Entry.objects.order_by('-pub_date')[:10]
    tags = Tag.objects.order_by('name')
    categories = {}
    category_counts = Category.objects.annotate(entry_count=Count('entry'))
    for category_rec in category_counts:
        categories[category_rec] = category_rec.entry_count

    context = {'tags': tags,
               'categories': categories,
               'recent_entries': recent_entries}
    if blog.disqus_shortname:
        #context['recent_comments'] = Disqus().get_post_list(blog.disqus_shortname)
        pass
    else:
        recent_comments = Comment.objects.order_by('-pub_date')[:7]
        context['recent_comments'] = recent_comments

    return context


def search(request):
    b = get_object_or_404(Blog, pk=1)
    if b.elastic_search_index and b.elastic_search_doc_type:
        return _es_search(request, b.elastic_search_index, b.elastic_search_doc_type)
    else:
        return _db_search(request)


def _db_search(request):
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string_base = request.GET['q']
        query_string = unicodedata.normalize('NFKC', query_string_base)
        entry_query = get_query(query_string, ['title', 'content'])
        found_entries = Entry.objects.filter(entry_query).order_by('-pub_date')
        context = {'query_string': query_string}
        return paginated_view(request, found_entries, html_file='blog/search.html', context=context)
    else:
        return index(request)


def _es_search(request, es_index, es_doc_type):
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        esc = escontrol.ESControl(es_index, es_doc_type)
        context = {'hit_list': esc.search_entries(query_string)}
        context.update(add_universal_content(request))
        return render(request, 'blog/search_es.html', context)
    else:
        raise Http404
