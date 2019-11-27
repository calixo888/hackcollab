from django.db import models
from django.contrib.auth.models import User
import uuid

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name="solarhacks_profile")
    id = models.IntegerField(unique=True, primary_key=True, blank=True)
    team_id = models.CharField(max_length=15, null=True, blank=True)
    birthday = models.DateField()
    school = models.CharField(max_length=100)
    gender = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=30, blank=True)
    # notification_type = models.CharField(max_length=10) # Email, phone, or both

    # Split each area with a tilda "~" into single string
    areas_of_expertise = models.TextField(blank=True)

    # Textarea input - users write a paragraph
    past_accomplishments = models.TextField(blank=True)

    # SOCIAL PROFILES
    github_link = models.CharField(max_length=50, blank=True)
    linkedin_link = models.CharField(max_length=50, blank=True)
    personal_website_link = models.CharField(max_length=50, blank=True)

    profile_picture = models.ImageField(blank=True, null=True)

    # SOFT SKILL RATINGS - rated from 1-10
    communication = models.IntegerField(blank=True)
    public_speaking = models.IntegerField(blank=True)
    teamwork = models.IntegerField(blank=True)
    leadership = models.IntegerField(blank=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Team(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=15)
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name


class Notification(models.Model):
    id = models.CharField(primary_key=True, max_length=30)
    title = models.CharField(max_length=50)
    description = models.TextField()
    source_id = models.CharField(max_length=15)
    target_id = models.CharField(max_length=15)
    type = models.CharField(max_length=10) # info or action

    def __str__(self):
        return self.title
