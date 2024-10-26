from django.forms import ModelForm
from apps.articles.models import *
from django.utils.html import strip_tags

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]

    def clean_content(self):
        content = self.cleaned_data["content"]
        return strip_tags(content)