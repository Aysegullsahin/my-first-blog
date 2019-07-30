from django import forms

from .models import Post, Category

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('category', 'title', 'text',)
