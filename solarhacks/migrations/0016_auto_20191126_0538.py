# Generated by Django 2.2.3 on 2019-11-26 05:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('solarhacks', '0015_auto_20191126_0309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='solarhacks_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
