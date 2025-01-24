from django.urls import path
from .views import news_detail, news_list, news_search, post_create, post_edit, post_delete, subscribe_to_category, category_detail

urlpatterns = [
    path('', news_list, name='news'),
    path('news/<int:pk>/', news_detail, name='news_detail'),
    path('news/search/', news_search, name='news_search'),
    path('news/create/', post_create, name='post_create'),
    path('news/<int:pk>/edit/', post_edit, name='post_edit'),
    path('news/<int:pk>/delete/', post_delete, name='post_delete'),
    path('subscribe/<int:category_id>/', subscribe_to_category, name='subscribe_to_category'),
    path('category/<int:category_id>/', category_detail, name='category_detail'),
]
