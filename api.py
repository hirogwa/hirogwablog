from bs4 import BeautifulSoup
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from models import Blog, Category, Entry
from search import get_query
import unicodedata


def entry_list(request, keyword):
    query_string_base = keyword
    query_string = unicodedata.normalize('NFKC', query_string_base)
    entry_query = get_query(query_string, ['title'])
    found_entries = Entry.objects.filter(entry_query).order_by('-pub_date')
    response = ''
    for entry_obj in found_entries:
        response += "%i, %s, %s\n" % (entry_obj.id, str(entry_obj.pub_date), entry_obj.title)

    return HttpResponse(response)


def entry(request, entry_id):
    entry_obj = get_object_or_404(Entry, pk=entry_id)
    return HttpResponse(entry_template(entry_id=int(entry_id),
                                       title=entry_obj.title,
                                       slug=entry_obj.slug,
                                       content=entry_obj.content,
                                       category=entry_obj.category.name,
                                       pub_date=entry_obj.pub_date))


@csrf_exempt
def entry_new(request):
    try:
        if request.method == 'GET':
            return HttpResponse(entry_template())

        elif request.method == 'POST':
            params_base = request.POST.get('body')
            params = BeautifulSoup(params_base)

            blog_obj = Blog.objects.get(pk=1)
            category_obj = get_object_or_404(Category, name=params.entry_category.get_text())

            entry_content = ''
            for child in params.entry_content.children:
                entry_content += str(child)

            entry_obj = Entry(blog=blog_obj,
                              title=params.entry_title.contents[0],
                              slug=params.entry_slug.get_text(),
                              category=category_obj,
                              content=entry_content,
                              pub_date=datetime.now()
                              )
            entry_obj.save()
            return HttpResponse('success')
    except Exception as e:
        return HttpResponseServerError(str(e))


@csrf_exempt
def entry_update(request):
    try:
        if request.method != 'POST':
            return HttpResponse('')

        params_base = request.POST.get('body')
        params = BeautifulSoup(params_base)

        target_entry = get_object_or_404(Entry, pk=int(params.entry_id.get_text()))
        category_obj = get_object_or_404(Category, name=params.entry_category.get_text())

        entry_content = ''
        for child in params.entry_content.children:
            entry_content += str(child)

        target_entry.title = params.entry_title.contents[0]
        target_entry.slug = params.entry_slug.get_text()
        target_entry.category = category_obj
        target_entry.content = entry_content

        target_entry.save()
        return HttpResponse('success')
    except Exception as e:
        return HttpResponseServerError(str(e))


def entry_template(entry_id=-1, title='', slug='', content='', category='', pub_date=None):
    response = 'body=' + '\n'
    response += '<entry_id>%d</entry_id>' % entry_id + '\n'
    response += '<entry_title>' + title + '</entry_title>' + '\n'
    response += '<entry_content>' + content + '</entry_content>' + '\n'
    response += '<entry_slug>' + slug + '</entry_slug>' + '\n'
    response += '<entry_category>' + category + '</entry_category>' + '\n'
    response += '<entry_pub_date>' + str(pub_date) + '</entry_pub_date>' + '\n'
    return response
