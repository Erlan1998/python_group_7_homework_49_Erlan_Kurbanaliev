from django.db import migrations

def apply_migration(apps, schema_editor):
    Profile = apps.get_model('accounts', 'Profile')
    User = apps.get_model('auth', 'User')

    for u in User.objects.filter(profile__isnull=True):
        Profile.objects.create(user=u)

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210416_1223'),
    ]

    operations = [
        migrations.RunPython(apply_migration, migrations.RunPython.noop)
    ]
