# serializers.py
from rest_framework import serializers

from apps.user.models import UserProfile
from .models import Post, User, Reply, Report

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']

class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer(read_only=True)  # Use the related name
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'userprofile']


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    is_liked = serializers.BooleanField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'like_count', 'reply_count', 'created_at', 'updated_at', 'is_liked']

class ReplySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    is_liked = serializers.BooleanField(read_only=True)
    post_id = serializers.UUIDField(source='post.id', read_only=True)

    class Meta:
        model = Reply
        fields = ['id', 'user', 'post_id', 'content', 'like_count', 'created_at', 'is_liked']


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'
