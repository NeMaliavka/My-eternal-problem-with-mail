from django import forms
from .models import Post, Author, Category

class PostForm(forms.ModelForm):
    author = forms.ModelChoiceField(queryset=Author.objects.all(), required=True)
    #categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Post
        fields = ['post_type', 'title', 'text', 'categories']
        widgets = {
            'categories': forms.CheckboxSelectMultiple(),}
