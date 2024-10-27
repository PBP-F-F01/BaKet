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

all_articles = Article.objects.all()
# Normalize the scores
max_like_score = all_articles.aggregate(max_like=models.Max('like_count'))['max_like']
max_comment_score = all_articles.aggregate(max_comment=models.Max('comment_count'))['max_comment']
def calculate_article_rank(article):
    global max_like_score
    global max_comment_score
    # Define weights for each factor
    like_weight = 20
    comment_weight = 15
    date_weight = 10

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
            date_weight * normalized_date_score +
            random.gauss((max_like_score + max_comment_score), (max_like_score + max_comment_score) / 100 + 1))

    return rank

ranked_articles = sorted(all_articles, key=calculate_article_rank, reverse=True)
def show_main(request):
    global ranked_articles
    global max_like_score
    global max_comment_score
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
        elif not search:
            articles = ranked_articles
    if not search and not sort:
        if len(ranked_articles) != articles.count():
            max_like_score = all_articles.aggregate(max_like=models.Max('like_count'))['max_like']
            max_comment_score = all_articles.aggregate(max_comment=models.Max('comment_count'))['max_comment']
            ranked_articles = sorted(articles, key=calculate_article_rank, reverse=True)

        articles = ranked_articles

    paginator = Paginator(articles, 10)  # Show 10 articles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'article_main.html', {'page_obj': page_obj})

def show_article(request, id):
    global ranked_articles
    article = Article.objects.get(pk=id)
    other = []
    for a in ranked_articles:
        if a != article:
            other.append(a)
        if len(other) >= 3:
            break

    # comment = Comment.objects.filter(article=article)
    # like_comment = Like.objects.filter(comment=comment)
    user_data = {
        'id': request.user.id,
        'is_anonymous': request.user.is_anonymous
    }
    context = {
        "article": article,
        "other": other,
        # "comment": comment,
        # "like_comment": like_comment,
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
    comment = Comment.objects.get(pk=comment_id)
    comment.delete()
    return HttpResponse(b"DELETED", status=201)

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
    return Like.objects.filter(user=request.user, article=Article.objects.get(pk=article_id)).exist()

def is_like_article_view(request, article_id):
    return JsonResponse({'is_like': is_like_article(request, article_id)})

def is_like_comment(request, comment_id):
    return Like.objects.filter(user=request.user, comment=Comment.objects.get(pk=comment_id)).exist()

def is_like_comment_view(request, comment_id):
    return JsonResponse({'is_like': is_like_comment(request, comment_id)})

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
    data = []

    for comment in comments:
        data.append({
            'pk': comment.pk,
            'fields': {
                'content': comment.content,
                'user': {
                    'username': comment.user.username,
                    'id': comment.user.id,
                    'is_anonymous': request.user.is_anonymous,
                },
                'created_at': comment.created_at,
                'has_edited': comment.has_edited,
                'like_count': comment.like_count
            }
        })

    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def json_like(request):
    data = Like.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def json_by_id_like(request, id):
    data = Article.objects.get(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")