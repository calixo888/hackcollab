# Generated by Django 2.2.3 on 2019-12-01 23:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hackathon',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('formal_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='HackathonIdentification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hackathon_name', models.CharField(max_length=30)),
                ('model_id', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='ID',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('generated_id', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('source_id', models.CharField(max_length=15)),
                ('target_id', models.CharField(max_length=15)),
                ('type', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.CharField(max_length=15, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('leader', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='TeamIdentification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_id', models.CharField(max_length=30)),
                ('user_id', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.CharField(blank=True, max_length=30, primary_key=True, serialize=False, unique=True)),
                ('birthday', models.DateField()),
                ('title', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=30)),
                ('phone_number', models.CharField(blank=True, max_length=30)),
                ('areas_of_expertise', models.TextField(blank=True)),
                ('past_accomplishments', models.TextField(blank=True)),
                ('github_link', models.CharField(blank=True, max_length=50)),
                ('linkedin_link', models.CharField(blank=True, max_length=50)),
                ('personal_website_link', models.CharField(blank=True, max_length=50)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='')),
                ('communication', models.IntegerField(blank=True)),
                ('public_speaking', models.IntegerField(blank=True)),
                ('teamwork', models.IntegerField(blank=True)),
                ('leadership', models.IntegerField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='testhacks_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
