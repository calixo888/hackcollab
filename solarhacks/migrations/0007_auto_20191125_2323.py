# Generated by Django 2.2.3 on 2019-11-25 23:23

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('solarhacks', '0006_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]
