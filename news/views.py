from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Category, User
from django.core.paginator import Paginator
from django_filters.views import FilterView
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@login_required
def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = category.post_set.all()  # Получаем все посты в этой категории
    return render(request, 'category_detail.html', {'category': category, 'posts': posts})

@login_required
def subscribe_to_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    user = request.user

    if user in category.subscribers.all():
        category.subscribers.remove(user)  # Отписка
    else:
        category.subscribers.add(user)  # Подписка

    return redirect('category_detail', category_id=category.id)  # Перенаправление на страницу категории

def news_list(request):
    post_news = Post.objects.order_by('created_at')
    paginator = Paginator(post_news, 2)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)
    
    template_name = 'news_list.html'
    return render(request, template_name, {'news': page_obj})  # Изменено на page_obj

def news_detail(request, pk):
    article = get_object_or_404(Post, id=pk)
    categories = article.categories.all()  # Получаем все категории, к которым относится статья
    return render(request, 'news_detail.html', {'article': article, 'categories': categories})


def news_search(request):
    post_filter = PostFilter(request.GET, queryset=Post.objects.filter(post_type=Post.NEWS))
    return render(request, 'news_search.html', {'filter': post_filter})


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user.author
            post.save()
            categories = form.cleaned_data.get('categories')
            if categories:
                post.categories.set(categories)

            # Отправка уведомлений подписчикам
            subscribers = post.categories.values_list('subscribers', flat=True)
            for subscriber in subscribers:
                user = User.objects.get(id=subscriber)
                html_content = render_to_string('new_article_notification.html', {'post': post, 'username': user.username})
                msg = EmailMultiAlternatives(
                    subject=post.title,
                    body=f"Здравствуй, {user.username}. Новая статья в твоём любимом разделе!",
                    from_email='alisermolova@yandex.ru',
                    to=[user.email],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()

            return redirect('news')  
    else:
        form = PostForm()

    return render(request, 'new_post.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('news_detail', pk=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'post_form.html', {'form': form})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, id=pk)
    post.delete()
    return redirect('news')

# def category_detail(request, category_id):
#     category = get_object_or_404(Category, id=category_id)
#     posts = category.post_set.all()  # Получаем все посты в этой категории
#     return render(request, 'category_detail.html', {'category': category, 'posts': posts})
