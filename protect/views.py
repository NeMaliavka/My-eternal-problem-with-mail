# from django.shortcuts import render
#
# from django.views.generic import TemplateView
# from django.contrib.auth.mixins import LoginRequiredMixin
#
#
# class IndexView(LoginRequiredMixin, TemplateView):
#     template_name = 'protect/index.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
#         return context
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from news.models import Category, Post  # Импортируйте Ваши модели

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        context['is_author'] = self.request.user.groups.filter(name='author').exists()
        context['categories'] = Category.objects.all()  # Получаем все категории
        context['latest_posts'] = Post.objects.order_by('-created_at')[:5]  # Получаем последние 5 новостей
        return context
