# Generated by Django 2.2.3 on 2019-11-27 05:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testhacks', '0019_remove_userprofile_notification_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='leader',
        ),
    ]