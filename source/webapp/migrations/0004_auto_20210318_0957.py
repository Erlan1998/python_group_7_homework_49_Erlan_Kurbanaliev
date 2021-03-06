# Generated by Django 3.1.7 on 2021-03-18 09:57

from django.db import migrations, models
import webapp.validators


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_auto_20210318_0950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='description',
            field=models.TextField(blank=True, max_length=3000, null=True, validators=[webapp.validators.MinLengthValidator(20)]),
        ),
        migrations.AlterField(
            model_name='list',
            name='summary',
            field=models.CharField(max_length=100, validators=[webapp.validators.MinLengthValidator(10)]),
        ),
    ]
