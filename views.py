from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from models import Entry, Blog, Category


PER_PAGE = 10


def index(request):
    return unfiltered(request)


def archive(request):
    entries = Entry.objects.all().order_by('-pub_date')
    context = {'entries': entries}
    return render(request, 'blog/archive.html', add_universal_content(context))


def page(request, entry_list):
    paginator = Paginator(entry_list, PER_PAGE)
    page_number = request.GET.get('page')
    try:
        entries = paginator.page(page_number)
    except PageNotAnInteger:
        entries = paginator.page(1)
    except EmptyPage:
        entries = paginator.page(paginator.num_pages)
    context = {'entries': entries}
    return render(request, 'blog/page.html', add_universal_content(context))


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
    return page(request, entries)


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
