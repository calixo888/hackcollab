# Generated by Django 2.2.3 on 2019-12-03 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hackathon', '0010_award'),
    ]

    operations = [
        migrations.AddField(
            model_name='award',
            name='hackathon_name',
            field=models.CharField(default='testhacks', max_length=20),
            preserve_default=False,
        ),
    ]
