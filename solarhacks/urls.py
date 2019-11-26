from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url("^$", views.index, name="index"),
    url("^register", views.register, name="register"),
    url("^login", views.user_login, name="login"),
    url("^logout", views.user_logout, name="logout"),
    url("^competitors", views.competitors, name="competitors"),
    url("^teams", views.teams, name="teams"),
    url("^notifications", views.notifications, name="notifications"),
    url("^create-team", views.create_team, name="create_team"),
    url(r'^profile/(?P<user_id>[^/]+)/$', views.view_profile, name='profile'),
    url(r'^team/(?P<team_id>[^/]+)/$', views.view_team, name='view_team'),
    url(r'^join-team/(?P<team_id>[^/]+)/$', views.join_team, name='join_team'),
    url(r'^leave-team/(?P<team_id>[^/]+)/$', views.leave_team, name='leave_team'),
    url(r'^invite-to-team', views.invite_to_team, name='invite_to_team'),
    url(r'^accept-user', views.accept_user, name="accept_user"),
    url(r'^reject-user', views.reject_user, name="reject_user"),
    url(r'^accept-invite', views.accept_invite, name="accept_invite"),
    url(r'^reject-invite', views.reject_invite, name="reject_invite"),
]
