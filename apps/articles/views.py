from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse
from apps.articles.models import *

# Create your views here.

def main(request):
    return render(request, 'article_main.html')

def dummy_article(request):
    return render(request, 'dummy_article.html')

def json(request):
    data = Article.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")