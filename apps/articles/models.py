from django.db import models
from django.contrib.auth.models import User
import uuid

class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=256)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    source = models.URLField(null=True, blank=True)
    like_count = 0
    comment_count = 0

    def inc_like(self):
        self.like_count += 1

    def dec_like(self):
        self.like_count -= 1

    def inc_comment(self):
        self.comment_count += 1

    def dec_comment(self):
        self.comment_count -= 1

    class Meta:
        ordering = ['-created_at']

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    has_edited = models.BooleanField(default=False)
    like_count = 0

    def inc_like(self):
        self.like_count += 1

    def dec_like(self):
        self.like_count -= 1
    
    class Meta:
        ordering = ['-created_at']

class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
