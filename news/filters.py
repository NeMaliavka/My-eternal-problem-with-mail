import django_filters
from .models import Post
from django import forms

class PostFilter(django_filters.FilterSet):
    created_at = django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    title = django_filters.CharFilter(lookup_expr='icontains', required=False)
    
    class Meta:
        model = Post
        fields = ['title', 'author__user__username', 'created_at']


