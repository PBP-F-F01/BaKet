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


# Get specific posts
def detail_post(request, id):
    post = Post.objects.get(pk=id)
    
    created_at = post.created_at.isoformat()
    updated_at = post.updated_at.isoformat()
    
    context = {
        'post': post,
        'anonymous': request.user.is_anonymous,
        'created_at': created_at,
        'updated_at': updated_at,
    }
    
    return render(request, 'detail_post.html', context)


# Processing tabs changes
def change_tabs(request, all_tabs='all'):
    response = HttpResponseRedirect(reverse('feeds:show_all'))
    response.set_cookie('last_tabs', all_tabs, max_age=3600)
    return response


###################
# POST MANAGEMENT #
###################


# Create a new post with AJAX
@csrf_exempt
@require_POST
def create_post(request):
    content = strip_tags(request.POST.get("content"))
    
    # Check if any of the fields are empty
    if not content:
        return HttpResponse(b"Missing required fields", status=400)

    new_product = Post(content=content.strip())
    
    new_product.save()

    return HttpResponse(b"Successfully Created", status=201)


# Show all Posts in JSON format
def post_json(request):
    data = Post.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


# Show all Posts by user in JSON format
def post_json_by_user(request, user=1):
    # data = Post.objects.filter(user=user)
    data = {}
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


# Show a Post filtered based on its ID in JSON
def post_json_by_id(request, id):
    data = Post.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


# See if user liked the given post
def is_liked(user, post): # Use UUID
    return Like.objects.filter(user=user, post=post).exists()


# Liked a post
def like_post(request, id):
    post = Post.objects.get(pk=id)
    
    if is_liked(request.user, post):
        return HttpResponse(b"Already Liked", status=400)
    
    new_like = Like(user=request.user, post=post)
    new_like.save()
    
    post.like_count += 1
    post.save()
    
    return HttpResponse(b"Successfully Liked", status=201)


# Unliked a post
def unlike_post(request, id):
    post = Post.objects.get(pk=id)
    
    if not is_liked(request.user, post):
        return HttpResponse(b"Already Unliked", status=400)
    
    Like.objects.filter(user=request.user, post=post).delete()
    
    post.like_count -= 1
    post.save()
    
    return HttpResponse(b"Successfully Unliked", status=201)


####################
# REPLY MANAGEMENT #
####################


# Create a new reply with AJAX
@csrf_exempt
@require_POST
def create_reply(request):
    post_id = request.POST.get("post_id")
    content = strip_tags(request.POST.get("content"))
    
    # Check if any of the fields are empty
    if not post_id or not content:
        return HttpResponse(b"Missing required fields", status=400)
    
    post = Post.objects.get(pk=post_id)
    new_reply = Reply(post=post, content=content.strip())
    
    new_reply.save()
    
    post.reply_count += 1
    post.save()
    
    return HttpResponse(b"Successfully Created", status=201)


# Show all Replies in JSON format
def reply_json(request, post_id):
    data = Reply.objects.filter(post=post_id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


# Show all Replies by user in JSON format
def reply_json_by_user(request, user=1, post_id=1):
    # data = Reply.objects.filter(user=user, post=post_id)
    data = {}
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


# Show a Reply filtered based on its ID in JSON
def reply_json_by_id(request, id):
    data = Reply.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


# See if user liked the given reply
def is_liked(user, post, reply): # Use UUID
    return Like.objects.filter(user=user, post=post, reply=reply).exists()


# Liked a reply
def like_reply(request, id):
    reply = Reply.objects.get(pk=id)
    
    if is_liked(request.user, reply):
        return HttpResponse(b"Already Liked", status=400)
    
    new_like = Like(user=request.user, reply=reply)
    new_like.save()
    
    reply.like_count += 1
    reply.save()
    
    return HttpResponse(b"Successfully Liked", status=201)


# Unliked a reply
def unlike_reply(request, id):
    reply = Reply.objects.get(pk=id)
    
    if not is_liked(request.user, reply):
        return HttpResponse(b"Already Unliked", status=400)
    
    Like.objects.filter(user=request.user, reply=reply).delete()
    
    reply.like_count -= 1
    reply.save()
    
    return HttpResponse(b"Successfully Unliked", status=201)