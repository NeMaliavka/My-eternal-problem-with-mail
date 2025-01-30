from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post


@receiver(post_save, sender=Post)
def my_handler(sender, instance, created, **kwargs):
    if created:
        # Выполнить действия после создания объекта MyModel
        print(f"Новый объект Post создан: {instance}")
