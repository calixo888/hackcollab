# Generated by Django 2.2.3 on 2019-12-03 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hackathon', '0009_teamsubmission'),
    ]

    operations = [
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('description', models.TextField()),
                ('team_id', models.CharField(max_length=15)),
            ],
        ),
    ]
