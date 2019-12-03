from django.contrib import admin
from . import models

class TeamAdmin(admin.ModelAdmin):
    writeonly_fields = ('id',)

admin.site.register(models.UserProfile, TeamAdmin)
admin.site.register(models.Team, TeamAdmin)
admin.site.register(models.Notification)
admin.site.register(models.ID)
admin.site.register(models.Hackathon)
admin.site.register(models.HackathonIdentification)
admin.site.register(models.TeamIdentification)
admin.site.register(models.TeamSubmission)
admin.site.register(models.Award)
