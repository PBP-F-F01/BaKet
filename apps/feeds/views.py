from datetime import datetime
import json
from django.urls import reverse
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import SessionAuthentication

from apps.feeds.models import *
from apps.feeds.pagination import PostPagination, ReplyPagination
from apps.feeds.serializer import *
from pytz import timezone

# csrf_exempt for mobile integration
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


# Get all the posts
def show_all(request):
    is_all = request.COOKIES.get('last_tabs', 'all') == 'all'

    context = {
        'date': datetime.now(timezone('Asia/Jakarta')).strftime("%A, %d %B %Y"),
        'tabs': is_all,
        'anonymous': request.user.is_anonymous,
        'user_id': request.user.id,
    }

    return render(request, 'feeds_page.html', context)


# Get specific posts
def detail_post(request, id):
    post = Post.objects.get(pk=id)

    created_at = post.created_at.isoformat()
    updated_at = post.updated_at.isoformat()
    
    try:
        is_user_post = request.user == post.user
        is_liked = Like.objects.filter(user=request.user, post=post).exists()
    except:
        is_user_post = False
        is_liked = False

    context = {
        'post': post,
        'anonymous': request.user.is_anonymous,
        'is_user_post': is_user_post,
        'is_liked': is_liked,
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
@login_required
def create_post(request):
    content = strip_tags(request.POST.get("content"))

    # Check if any of the fields are empty
    if not content:
        return HttpResponse(b"Missing required fields", status=400)

    new_product = Post(content=content.strip(), user=request.user)
    new_product.save()

    return HttpResponse(b"Successfully Created", status=201)


# Update a post
@csrf_exempt
@login_required
def edit_post(request, id):
    post = Post.objects.get(pk=id)
    if request.user != post.user:
        return HttpResponse(b"Unauthorized", status=401)

    post.content = strip_tags(request.POST.get("content"))
    post.save()

    return HttpResponse(b"Successfully Updated", status=201)


# Delete a post
@csrf_exempt
@login_required
def delete_post(request, id):
    post = Post.objects.get(pk=id)
    if request.user != post.user:
        return HttpResponse(b"Unauthorized", status=401)

    post.delete()

    return HttpResponse(b"Successfully Deleted", status=204)


# Show all Posts in JSON format
@api_view(['GET'])
def post_json(request):
    query = request.GET.get('q', '')
    
    if request.user.is_authenticated:
        data = Post.objects.filter(
            content__icontains=query
        ).annotate(
            is_liked=models.Exists(Like.objects.filter(
                user=request.user, post=models.OuterRef('pk')))
        )
    else:
        data = Post.objects.filter(
            content__icontains=query
        ).annotate(
            is_liked=models.Value(False, output_field=models.BooleanField())
        )
    
    serializer = PostSerializer(data, many=True)
    return Response(serializer.data)


# Show all Posts by user in JSON format
@api_view(['GET'])
def post_json_by_user(request, user):
    query = request.GET.get('q', '')
    
    if request.user.is_authenticated:
        data = Post.objects.filter(
            content__icontains=query, user=user
        ).annotate(
            is_liked=models.Exists(Like.objects.filter(
                user=request.user, post=models.OuterRef('pk')))
        )
    else:
        data = Post.objects.filter(
            content__icontains=query, user=user
        ).annotate(
            is_liked=models.Value(False, output_field=models.BooleanField())
        )
    
    serializer = PostSerializer(data, many=True)
    return Response(serializer.data)


# Show a Post filtered based on its ID in JSON
@api_view(['GET'])
def post_json_by_id(request, id):
    data = Post.objects.filter(pk=id)
    serializer = PostSerializer(data, many=True)
    return Response(serializer.data)


# Liked a post
@csrf_exempt
@login_required(login_url='/login/')
def like_post(request, id):
    post = Post.objects.get(pk=id)

    if Like.objects.filter(user=request.user, post=post).exists():
        return HttpResponse(b"Already Liked", status=400)

    new_like = Like(user=request.user, post=post)
    new_like.save()

    post.like_count = Like.objects.filter(post=post).count()
    post.save()

    return HttpResponse(b"Successfully Liked", status=201)


# Unliked a post
@csrf_exempt
@login_required(login_url='/login/')
def unlike_post(request, id):
    post = Post.objects.get(pk=id)

    if not Like.objects.filter(user=request.user, post=post).exists():
        return HttpResponse(b"Already Unliked", status=400)

    Like.objects.filter(user=request.user, post=post).delete()

    post.like_count = Like.objects.filter(post=post).count()
    post.save()

    return HttpResponse(b"Successfully Unliked", status=201)


####################
# REPLY MANAGEMENT #
####################


# Create a new reply with AJAX
@csrf_exempt
@require_POST
@login_required
def create_reply(request):
    post_id = request.POST.get("post_id")
    content = strip_tags(request.POST.get("content"))

    # Check if any of the fields are empty
    if not post_id or not content:
        return HttpResponse(b"Missing required fields", status=400)

    post = Post.objects.get(pk=post_id)
    new_reply = Reply(post=post, content=content.strip(), user=request.user)

    new_reply.save()

    post.reply_count += 1
    post.save()

    return HttpResponse(b"Successfully Created", status=201)


# Delete a reply
@login_required
def delete_reply(request, id):
    reply = Reply.objects.get(pk=id)
    if request.user != reply.user:
        return HttpResponse(b"Unauthorized", status=401)

    reply.delete()

    return HttpResponse(b"Successfully Deleted", status=204)


# Show all Replies in JSON format
@api_view(['GET'])
def reply_json(request, post_id):
    data = Reply.objects.filter(post=post_id).annotate(
        is_liked=models.Exists(Like.objects.filter(
            user=request.user, reply=models.OuterRef('pk')))
    ) if request.user.is_authenticated else Reply.objects.filter(post=post_id).annotate(
        is_liked=models.Value(False, output_field=models.BooleanField())
    )
    serializer = ReplySerializer(data, many=True)
    return Response(serializer.data)


# Show all Replies by user in JSON format
@api_view(['GET'])
def reply_json_by_user(request, user, post_id):
    data = Reply.objects.filter(user=user, post=post_id)
    serializer = ReplySerializer(data, many=True)
    return Response(serializer.data)


# Show a Reply filtered based on its ID in JSON
@api_view(['GET'])
def reply_json_by_id(request, id):
    data = Reply.objects.filter(pk=id)
    serializer = ReplySerializer(data, many=True)
    return Response(serializer.data)


# Liked a reply
@csrf_exempt
@login_required(login_url='/login/')
def like_reply(request, id):
    reply = Reply.objects.get(pk=id)
    post = reply.post

    if Like.objects.filter(user=request.user, reply=reply).exists():
        return HttpResponse(b"Already Liked", status=400)

    new_like = Like(user=request.user, reply=reply, post=post)
    new_like.save()

    reply.like_count = Like.objects.filter(reply=reply).count()
    reply.save()

    return HttpResponse(b"Successfully Liked", status=201)


# Unliked a reply
@csrf_exempt
@login_required(login_url='/login/')
def unlike_reply(request, id):
    reply = Reply.objects.get(pk=id)

    if not Like.objects.filter(user=request.user, reply=reply).exists():
        return HttpResponse(b"Already Unliked", status=400)

    Like.objects.filter(user=request.user, reply=reply).delete()

    reply.like_count = Like.objects.filter(reply=reply).count()
    reply.save()

    return HttpResponse(b"Successfully Unliked", status=201)


#################
# REPORT SYSTEM #
#################


# Report a post or reply
@csrf_exempt
@require_POST
def report(request):
    reporting = request.POST.get("id")
    report_type = request.POST.get("type")

    # Check if any of the fields are empty
    if not report_type:
        return HttpResponse(b"Missing required fields", status=400)

    new_report = Report(reporting=reporting, report_type=report_type)
    new_report.save()

    return HttpResponse(b"Successfully Reported", status=201)


@api_view(['GET'])
def report_json(request):
    data = Report.objects.all()
    serializer = ReportSerializer(data, many=True)
    return Response(serializer.data)


################
# MOBILE INTEG #
################


# Create a new post for mobile app
@csrf_exempt
@api_view(['POST'])
@authentication_classes([CsrfExemptSessionAuthentication])
def create_post_mobile(request):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "User not authenticated"}, status=401)
    
    try:
        data = json.loads(request.body)
        new_mood = Post.objects.create(
            user=request.user,
            content=data['content']
        )

        new_mood.save()
    except:
        return JsonResponse({"status": "Failed to add post"}, status=400)

    return JsonResponse({"status": "Successfully added post"}, status=200)
    

# Update a post for mobile app
@csrf_exempt
@api_view(['POST'])
@authentication_classes([CsrfExemptSessionAuthentication])
def edit_post_mobile(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "User not authenticated"}, status=401)
    
    try:
        post = Post.objects.get(pk=id)
        if request.user != post.user:
            return JsonResponse({"status": "Wrong user"}, status=401)
        
        data = json.loads(request.body)
        post.content = data['content']
        post.save()
    except:
        return JsonResponse({"status": "Failed to update post"}, status=400)

    return JsonResponse({"status": "Successfully updated post"}, status=200)


# Delete a post for mobile app
@csrf_exempt
@api_view(['POST'])
@authentication_classes([CsrfExemptSessionAuthentication])
def delete_post_mobile(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "User not authenticated"}, status=401)
    
    post = Post.objects.get(pk=id)
    
    if not post:
        return JsonResponse({"status": "Post not found"}, status=404)
    
    if request.user != post.user:
        return JsonResponse({"status": "Wrong user"}, status=401)

    post.delete()

    return JsonResponse({"status": "Successfully deleted post"}, status=200)


# Like a post from mobile app
@csrf_exempt
@api_view(['POST'])
@authentication_classes([CsrfExemptSessionAuthentication])
def like_post_mobile(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "User not authenticated"}, status=401)
    
    post = Post.objects.get(pk=id)
    
    if not post:
        return JsonResponse({"status": "Post not found"}, status=404)

    if Like.objects.filter(user=request.user, post=post).exists():
        return JsonResponse({"status": "Already liked"}, status=400)

    new_like = Like(user=request.user, post=post)
    new_like.save()

    post.like_count = Like.objects.filter(post=post).count()
    post.save()

    return JsonResponse({"status": "Successfully liked"}, status=201)


# Unlike a post from mobile app
@csrf_exempt
@api_view(['POST'])
@authentication_classes([CsrfExemptSessionAuthentication])
def unlike_post_mobile(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "User not authenticated"}, status=401)
    
    post = Post.objects.get(pk=id)
    
    if not post:
        return JsonResponse({"status": "Post not found"}, status=404)

    if not Like.objects.filter(user=request.user, post=post).exists():
        return JsonResponse({"status": "Already unliked"}, status=400)

    Like.objects.filter(user=request.user, post=post).delete()

    post.like_count = Like.objects.filter(post=post).count()
    post.save()

    return JsonResponse({"status": "Successfully unliked"}, status=201)


# Create reply from mobile app
@csrf_exempt
@api_view(['POST'])
@authentication_classes([CsrfExemptSessionAuthentication])
def create_reply_mobile(request):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "User not authenticated"}, status=401)
    
    try:
        data = json.loads(request.body)
        
        post = Post.objects.get(pk=data['post_id'])
        if not post:
            return JsonResponse({"status": "Post not found"}, status=404)
    
        reply = Reply.objects.create(
            user=request.user,
            post=post,
            content=data['content']
        )

        reply.save()
    except:
        return JsonResponse({"status": "Failed to add reply"}, status=400)

    post.reply_count += 1
    post.save()

    return JsonResponse({"status": "Successfully added reply"}, status=200)


# Delete a reply from mobile
@csrf_exempt
@api_view(['POST'])
@authentication_classes([CsrfExemptSessionAuthentication])
def delete_reply_mobile(request):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "User not authenticated"}, status=401)
    
    try:
        data = json.loads(request.body)
        reply = Reply.objects.get(pk=data['reply_id'])
        
        if not reply:
            return JsonResponse({"status": "Reply not found"}, status=404)
        
        if request.user != reply.user:
            return JsonResponse({"status": "Wrong user"}, status=401)
        
        reply.delete()
    except:
        return JsonResponse({"status": "Failed to delete reply"}, status=400)
    
    post = reply.post
    post.reply_count -= 1
    post.save()
    
    return JsonResponse({"status": "Successfully deleted reply"}, status=200)


# Like a reply from mobile
@csrf_exempt
@api_view(['POST'])
@authentication_classes([CsrfExemptSessionAuthentication])
def like_reply_mobile(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "User not authenticated"}, status=401)
    
    reply = Reply.objects.get(pk=id)
    
    if not reply:
        return JsonResponse({"status": "Reply not found"}, status=404)
    
    if Like.objects.filter(user=request.user, reply=reply).exists():
        return JsonResponse({"status": "Already liked"}, status=400)

    post = reply.post

    new_like = Like(user=request.user, reply=reply, post=post)
    new_like.save()

    reply.like_count = Like.objects.filter(reply=reply).count()
    reply.save()

    return JsonResponse({"status": "Successfully liked"}, status=201)


# Unlike a reply from mobile
@csrf_exempt
@api_view(['POST'])
@authentication_classes([CsrfExemptSessionAuthentication])
def unlike_reply_mobile(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "User not authenticated"}, status=401)
    
    reply = Reply.objects.get(pk=id)
    
    if not reply:
        return JsonResponse({"status": "Reply not found"}, status=404)
    
    if not Like.objects.filter(user=request.user, reply=reply).exists():
        return JsonResponse({"status": "Already unliked"}, status=400)

    Like.objects.filter(user=request.user, reply=reply).delete()

    reply.like_count = Like.objects.filter(reply=reply).count()
    reply.save()

    return JsonResponse({"status": "Successfully unliked"}, status=201)


# Report a post from mobile
@csrf_exempt
@api_view(['POST'])
@authentication_classes([CsrfExemptSessionAuthentication])
def report_mobile(request):
    try:
        data = json.loads(request.body)
        
        if not data['reporting'] or not data['report_type']:
            return JsonResponse({"status": "Missing required fields"}, status=400)
        
        new_report = Report(reporting=data['reporting'], report_type=data['report_type'])
        new_report.save()
    except:
        return JsonResponse({"status": "Failed to report"}, status=400)

    return JsonResponse({"status": "Successfully reported"}, status=201)


###############
# PAGINATIONS #
###############


# Get all the posts with pagination (post_json for mobile)
@csrf_exempt
@api_view(['GET'])
def api_post_json(request):
    query = request.GET.get('q', '')
    paginator = PostPagination()
    
    if request.user.is_authenticated:
        data = Post.objects.filter(
            content__icontains=query
        ).annotate(
            is_liked=models.Exists(Like.objects.filter(
                user=request.user, post=models.OuterRef('pk')))
        )
    else:
        data = Post.objects.filter(
            content__icontains=query
        ).annotate(
            is_liked=models.Value(False, output_field=models.BooleanField())
        )
    
    # Paginate
    result_page = paginator.paginate_queryset(data, request)
    serializer = PostSerializer(result_page, many=True)
    
    return paginator.get_paginated_response(serializer.data)


# Get all Post by user paginated
@csrf_exempt
@api_view(['GET'])
def api_post_json_by_user(request):
    query = request.GET.get('q', '')
    paginator = PostPagination()
    
    data = Post.objects.filter(
        content__icontains=query, user=request.user
    ).annotate(
        is_liked=models.Exists(Like.objects.filter(
            user=request.user, post=models.OuterRef('pk')))
    ) if request.user.is_authenticated else Post.objects.filter(user=request.user).annotate(
        is_liked=models.Value(False, output_field=models.BooleanField())
    )
    
    # Paginate
    result_page = paginator.paginate_queryset(data, request)
    serializer = PostSerializer(result_page, many=True)
    
    return paginator.get_paginated_response(serializer.data)    


# Get all reply with pagination
@csrf_exempt
@api_view(['GET'])
def api_reply_json(request, post_id):
    paginator = ReplyPagination()
    
    data = Reply.objects.filter(post=post_id).annotate(
        is_liked=models.Exists(Like.objects.filter(
            user=request.user, reply=models.OuterRef('pk')))
    ) if request.user.is_authenticated else Reply.objects.filter(post=post_id).annotate(
        is_liked=models.Value(False, output_field=models.BooleanField())
    )
    
    # Paginate
    result_page = paginator.paginate_queryset(data, request)
    serializers = ReplySerializer(result_page, many=True)
    
    return paginator.get_paginated_response(serializers.data)