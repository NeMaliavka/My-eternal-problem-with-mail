from django.db import models

ADMINISTRATOR = 'AD'
AUTOR_NEWS = 'AN'
NORMAL_USER = 'NU'

roles = [
    (ADMINISTRATOR, 'Администратор'),
    (AUTOR_NEWS, 'Автор статей'),
    (NORMAL_USER, 'Пользователь')
]


class User(models.Model):
    user_name = models.CharField(max_length=255)
    role = models.CharField(max_length=2,
                            choices=roles,
                            default=NORMAL_USER)
