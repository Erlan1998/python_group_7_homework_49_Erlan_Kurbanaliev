from django.db import models
from webapp.validators import MinLengthValidator, CapitalLetter


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


class List(models.Model):
    summary = models.CharField(max_length=100, null=False, blank=False, validators=(MinLengthValidator(10), CapitalLetter))
    description = models.TextField(max_length=3000, null=False, blank=False, validators=(MinLengthValidator(20),))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.ForeignKey('webapp.Status', related_name='Lists', on_delete=models.PROTECT)
    tip = models.ManyToManyField('webapp.Type', related_name='Lists',  blank=True)

    class Meta:
        db_table = 'Lists'
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return f'{self.id}. {self.status}: {self.description}'