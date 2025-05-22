from django.db import migrations

def create_default_site(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    # Delete everything except id=1 (to prevent duplicate or irrelevant sites)
    Site.objects.exclude(id=1).delete()
    Site.objects.update_or_create(
        id=1,
        defaults={
            'domain': 'gentle-gratitude-production.up.railway.app',
            'name': 'Railway'
        }
    )
#gentle-gratitude-production.up.railway.app
#Railway
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
