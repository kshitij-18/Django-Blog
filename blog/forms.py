from django import forms
from django.forms import ModelForm
from . models import article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = article
        fields = ('title', 'description', 'article_image', 'category')
