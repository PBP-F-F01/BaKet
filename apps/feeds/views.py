from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags

from apps.feeds.models import *


# Get all the posts
def show_all(request):
    return render(request, 'feeds_page.html')


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
