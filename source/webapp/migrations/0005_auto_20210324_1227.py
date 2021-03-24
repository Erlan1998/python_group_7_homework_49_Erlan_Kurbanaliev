# Generated by Django 3.1.7 on 2021-03-24 12:27

from django.db import migrations, models
import webapp.validators


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_auto_20210318_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='description',
            field=models.TextField(max_length=3000, validators=[webapp.validators.MinLengthValidator(20), webapp.validators.CapitalLetter]),
        ),
        migrations.AlterField(
            model_name='list',
            name='summary',
            field=models.CharField(max_length=100, validators=[webapp.validators.MinLengthValidator(3), webapp.validators.OnlyLetters, webapp.validators.CapitalLetter]),
        ),
    ]
