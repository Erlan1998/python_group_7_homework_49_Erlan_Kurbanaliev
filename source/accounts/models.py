from django.contrib.auth import get_user_model
from django.db import models



class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), related_name='profile', on_delete=models.CASCADE, verbose_name='Пользователь', null=True)
    avatar = models.ImageField(null=True, blank=True, upload_to='user_pics', verbose_name='Аватар')
    github = models.URLField(max_length=250, blank=True, null=True, verbose_name='Ссылка на Github:')
    about = models.TextField(max_length=150, null=True, blank=True, verbose_name='О себе:')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        permissions = [
            ('user_view', 'просмотр пользователей!')
        ]

