from django.contrib import admin
from . import models

class TeamAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(models.UserProfile, TeamAdmin)
admin.site.register(models.Team, TeamAdmin)
admin.site.register(models.Notification)