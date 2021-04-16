from django.db import models



class Profile(models.Model):
    avatar = models.ImageField(null=True, blank=True, upload_to='user_pics', verbose_name='Аватар')
    github = models.URLField(max_length=250, blank=True, null=True)
    about = models.TextField(max_length=150, null=True, blank=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
