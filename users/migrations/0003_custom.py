from django.db import migrations

def create_default_site(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    Site.objects.get_or_create(
        id=1,
        defaults={
            'domain': '127.0.0.1:8000',
            'name': 'localhost'
        }
    )

def remove_default_site(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    Site.objects.filter(id=1).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.RunPython(create_default_site, remove_default_site),
    ]