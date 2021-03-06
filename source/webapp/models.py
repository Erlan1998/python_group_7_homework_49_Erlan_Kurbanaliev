from django.db import models
from webapp.validators import MinLengthValidator, CapitalLetter, OnlyLetters
from django.contrib.auth import get_user_model


class Status(models.Model):
    status = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return f'{self.status}'


class Type(models.Model):
    tip = models.CharField(max_length=50, null=False, blank=False, verbose_name='Тип')

    class Meta:
        db_table = 'types'
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'

    def __str__(self):
        return f'{self.tip}'


class Projects(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    created_date = models.DateField(null=False, blank=False, verbose_name='Дата Начало')
    update_date = models.DateField(null=True, blank=True, verbose_name='Дата Окончания')
    user = models.ManyToManyField(get_user_model(), default=1, related_name='projects', verbose_name='пользователи')

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        permissions = [
            ('user_project_add', 'может добавлть пользователя')
        ]

    def __str__(self):
        return f'{self.name}'


class List(models.Model):
    summary = models.CharField(max_length=100, null=False, blank=False, validators=(MinLengthValidator(3), OnlyLetters, CapitalLetter))
    description = models.TextField(max_length=3000, null=False, blank=False, validators=(MinLengthValidator(20), CapitalLetter))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.ForeignKey('webapp.Status', related_name='Lists', on_delete=models.PROTECT)
    tip = models.ManyToManyField('webapp.Type', related_name='Lists',  blank=True)
    project = models.ForeignKey('webapp.Projects', related_name='Lists', on_delete=models.CASCADE)

    class Meta:
        db_table = 'Lists'
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return f'{self.id}. {self.status}: {self.description}'