import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, Category
from celery import shared_task
from django.conf import settings


@shared_task
def send_email_task(pk, preview):
    post = Post.objects.get(pk=pk)
    categories = post.category.all()
    title = post.title
    subscribers_emails = []

    for categ in categories:
        subscribers_users = categ.subscribers.all()
        for sub_users in subscribers_users:
            subscribers_emails.append(sub_users.email)

    html_content = render_to_string(
        'post_created_email_task.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/post/{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[subscribers_emails],

    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def week_send_email_task():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(time_post__gte=last_week)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
        'flatpages/daily_post.html',
        {
            'link': settings.SITE_URL,
            'post': posts
        }
    )

    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
