# Generated by Django 3.1.7 on 2021-03-26 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_porjects'),
    ]

    operations = [
        migrations.AlterField(
            model_name='porjects',
            name='created_date',
            field=models.DateField(verbose_name='Начало'),
        ),
        migrations.AlterField(
            model_name='porjects',
            name='update_date',
            field=models.DateField(blank=True, null=True, verbose_name='Окончание'),
        ),
    ]