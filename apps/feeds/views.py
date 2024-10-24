from datetime import datetime
from django.urls import reverse
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags

from apps.feeds.models import *
from pytz import timezone


# Get all the posts
def show_all(request):
    is_all = request.COOKIES.get('last_tabs', 'all') == 'all'
    
    posts = Post.objects.all() if is_all else Post.objects.filter(like_count__gt=0)
    
    context = {
        'date': datetime.now(timezone('Asia/Jakarta')).strftime("%A, %d %B %Y"),
        'tabs': is_all,
        'posts': posts,
        'anonymous': request.user.is_anonymous
    }
    
    return render(request, 'feeds_page.html', context)


# Processing tabs changes
def change_tabs(request, all_tabs='all'):
    response = HttpResponseRedirect(reverse('feeds:show_all'))
    response.set_cookie('last_tabs', all_tabs, max_age=3600)
    return response


# Create a new post with AJAX
@csrf_exempt
@require_POST
def create_post(request):
    content = strip_tags(request.POST.get("content"))
    
    # Check if any of the fields are empty
    if not content:
        return HttpResponse(b"Missing required fields", status=400)

    new_product = Post(content=content)
    
    new_product.save()

    return HttpResponse(b"Successfully Created", status=201)


# Show all Posts in JSON format
def json(request):
    data = Post.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


# Show a Post filtered based on its ID in JSON
def json_by_id(request, id):
    data = Post.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
