from django.shortcuts import render
from django.core import serializers
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.db.models import F
from apps.articles.models import *
import datetime
import random
import math
import json

# Create your views here.

def artic_main(request):
    return render(request, 'artic_main.html')

def dummy_article(request):
    return render(request, 'dummy_article.html')

def dummy_main(request):
    return render(request, 'dummy_main.html')

def calculate_article_rank(article):
    max_like_score = get_max_like_score()
    max_comment_score = get_max_comment_score()
    
    # Define weights for each factor
    like_weight = 20
    comment_weight = 16
    date_weight = 4

    # Calculate the score for each factor
    like_score = article.like_count
    comment_score = article.comment_count
    date_score = (datetime.datetime.now(datetime.timezone.utc) - article.created_at).days

    normalized_like_score = like_score / max_like_score if max_like_score != 0 else 0
    normalized_comment_score = comment_score / max_comment_score if max_comment_score != 0 else 0
    normalized_date_score = math.exp(-1 * date_score) # More recent articles get higher score

    # Calculate the final rank
    rank = (like_weight * normalized_like_score +
            comment_weight * normalized_comment_score +
            date_weight * normalized_date_score)

    return rank

def show_main(request):
    articles = Article.objects.all()
    
    if articles.count() == 0:
        return render(request, 'article_main.html', {'page_obj': None})
    search = request.GET.get("search")
    sort = request.GET.get("sort")
    if search:
        articles = articles.filter(title__icontains=search)
    if sort:
        if sort == "most_like":
            articles = articles.order_by("-like_count")
        elif sort == "oldest":
            articles = articles.order_by("created_at")
        elif sort == "most_recent":
            articles = articles.order_by("-created_at")
    if not search and not sort:
        articles = sorted(articles, key=calculate_article_rank, reverse=True)

    paginator = Paginator(articles, 10)  # Show 10 articles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'article_main.html', {'page_obj': page_obj})

def show_article(request, id):
    articles = ranked_articles()
    
    article = Article.objects.get(pk=id)
    other = []
    for a in articles:
        if a != article:
            other.append(a)
        if len(other) >= 3:
            break

    user_data = {
        'id': request.user.id,
        'is_anonymous': request.user.is_anonymous
    }
    context = {
        "article": article,
        "other": other,
        "anonymous": request.user.is_anonymous,
        "user_data": json.dumps(user_data)
    }
    return render(request, 'article.html', context=context)

@csrf_exempt
@require_POST
def add_comment(request, article_id):
    if request.user.is_authenticated:
        data = json.loads(request.body)
        content = strip_tags(data.get("content"))
        article = Article.objects.get(pk=article_id)

        new_comment = Comment(
            content=content,
            article=article,
            user=request.user
        )

        new_comment.save()
        return JsonResponse({
            'id': new_comment.id,
            'text': new_comment.content,
            'author': new_comment.user.username,
            'created_at': new_comment.created_at.isoformat()
        }, status=201)
    return JsonResponse({}, status=401)

def update_comment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    comment.content = strip_tags(request.PATCH.get("content"))
    comment.has_edited = True
    comment.save()
    return HttpResponse(b"UPDATED", status=201)

def delete_comment(request, comment_id):
    if request.method == "DELETE":
        comment = Comment.objects.get(pk=comment_id)
        comment.delete()
        return HttpResponse(b"DELETED", status=201)
    return HttpResponse(b"FORBIDDEN", status=403)

def like_article(request, article_id):
    if request.user.is_authenticated:
        article = Article.objects.get(pk=article_id)
        if not is_like_article(request, article):
            Like.objects.create(user=request.user, article=article)
        return HttpResponse(b"LIKED", status=201)
    return HttpResponse(b"not authenticated", status=401)

def unlike_article(request, article_id):
    if request.user.is_authenticated:
        article = Article.objects.get(pk=article_id)
        if is_like_article(request, article):
            Like.objects.filter(user=request.user, article=article).delete()
        return HttpResponse(b"UNLIKED", status=201)
    return HttpResponse(b"not authenticated", status=401)

def like_comment(request, comment_id):
    if request.user.is_authenticated:
        comment = Comment.objects.get(pk=comment_id)
        if not is_like_comment(request, comment):
            Like.objects.create(user=request.user, comment=comment)
        return HttpResponse(b"LIKED", status=201)
    return HttpResponse(b"not authenticated", status=401)

def unlike_comment(request, comment_id):
    if request.user.is_authenticated:
        comment = Comment.objects.get(pk=comment_id)
        if is_like_comment(request, comment):
            Like.objects.filter(user=request.user, comment=comment).delete()
        return HttpResponse(b"UNLIKED", status=201)
    return HttpResponse(b"not authenticated", status=401)

def current_user(request):
    user_data = {
        'id': request.user.id,
        'is_anonymous': request.user.is_anonymous
    }
    return HttpResponse(json.dumps(user_data), content_type="application/json")

def is_like_article(request, article_id):
    return Like.objects.filter(user=request.user, article=Article.objects.get(pk=article_id)).exists()

def is_like_article_view(request, article_id):
    return JsonResponse({'is_like': is_like_article(request, article_id)})

def is_like_comment(request, comment_id):
    return Like.objects.filter(user=request.user, comment=Comment.objects.get(pk=comment_id)).exists()

def is_like_comment_view(request, comment_id):
    return JsonResponse({'is_like': is_like_comment(request, comment_id)})

def is_comment_article(request, article_id):
    return Comment.objects.filter(user=request.user, article=Article.objects.get(pk=article_id)).exists()

def json_article(request):
    data = Article.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def json_by_id_aricle(request, id):
    data = Article.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def json_comment(request):
    data = Comment.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def json_by_id_comment(request, id):
    data = Comment.objects.comment(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def json_comment_by_article(request, article_id):
    comments = Comment.objects.filter(article=Article.objects.get(pk=article_id))
    data = comments

    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def json_like(request):
    data = Like.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def json_by_id_like(request, id):
    data = Article.objects.get(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


# Helper Functions (ijin ubah ya yasin) ## Aman - yasin
def get_max_like_score():
    return Article.objects.all().aggregate(max_like=models.Max('like_count'))['max_like']
    
def get_max_comment_score():
    return Article.objects.all().aggregate(max_comment=models.Max('comment_count'))['max_comment']
    
def ranked_articles():
    return sorted(Article.objects.all(), key=calculate_article_rank, reverse=True)

# For Flutter

def json_article_flutter(request):
    articles = Article.objects.all()
    
    if articles.count() == 0:
        return render(request, 'article_main.html', {'page_obj': None})
    search = request.GET.get("search")
    sort = request.GET.get("sort")
    if search:
        articles = articles.filter(title__icontains=search)
    if sort:
        if sort == "most_like":
            articles = articles.order_by("-like_count")
        elif sort == "oldest":
            articles = articles.order_by("created_at")
        elif sort == "most_recent":
            articles = articles.order_by("-created_at")
    if not search and not sort:
        articles = sorted(articles, key=calculate_article_rank, reverse=True)

    data = []
    for a in articles:
        data.append({
            "id": a.id,
            "title": a.title,
            "posted_by": a.posted_by,
            "like_count": a.like_count,
            "comment_count": a.comment_count,
            "is_like": is_like_article(request, a.id),
            "is_comment": is_comment_article(request, a.id),
        })
    return JsonResponse(data, safe=False)