from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),

    # Regular URLs
    url("^$", views.index, name="index"),
    url("^register/$", views.register, name="register"),
    url("^login/$", views.user_login, name="login"),
    url("^logout/$", views.user_logout, name="logout"),
    url("^update/$", views.update, name="update"),
    url("^hackathon-info/$", views.hackathon_info, name="hackathon_info"),
    url("^competitors/$", views.competitors, name="competitors"),
    url("^teams/$", views.teams, name="teams"),
    url("^notifications/$", views.notifications, name="notifications"),
    url("^contact-support/$", views.contact_support, name="contact_support"),
    url("^success/$", views.success, name="success"),
    url("^create-team/$", views.create_team, name="create_team"),
    url(r'^profile/(?P<user_id>[^/]+)/$', views.view_profile, name='profile'),
    url(r'^view-team/(?P<team_id>[^/]+)/$', views.view_team, name='view_team'),
    url(r'^team/(?P<team_id>[^/]+)/$', views.team, name='team'),
    url(r'^join-team/(?P<team_id>[^/]+)/$', views.join_team, name='join_team'),
    url(r'^leave-team/(?P<team_id>[^/]+)/$', views.leave_team, name='leave_team'),
    url(r'^invite-to-team', views.invite_to_team, name='invite_to_team'),
    url(r'^submit/$', views.submit, name="submit"),
    url(r'^awards/$', views.awards, name="awards"),
    url(r'^team-submissions/$', views.submissions, name="submissions"),
    url(r'^select-team/$', views.select_team, name="select_team"),
    # STAFF VIEWS
    url("^modify-hackathon-info/$", views.modify_hackathon_info, name="modify_hackathon_info"),
    url("^admin-view/$", views.admin_view, name="admin_view"),
    # POST REQUEST
    url(r'^accept-user', views.accept_user, name="accept_user"),
    url(r'^reject-user', views.reject_user, name="reject_user"),
    url(r'^accept-invite', views.accept_invite, name="accept_invite"),
    url(r'^reject-invite', views.reject_invite, name="reject_invite"),
    url(r'^delete-user', views.delete_user, name="delete_user"),
    url(r'^delete-team', views.delete_team, name="delete_team"),
    url(r'^delete-notification', views.delete_notification, name="delete_notification"),
    url(r'^delete-submission', views.delete_submission, name="delete_submission"),
    url(r'^delete-award', views.delete_award, name="delete_award"),
    url(r'^kickout', views.kickout, name="kickout"),
    url(r'^assign-award', views.assign_award, name="assign_award"),

    # Password reset URLs
    url('^', include('django.contrib.auth.urls')),

    # Serving static and media assets
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'hackcollab_app.views.handler404'
handler500 = 'hackcollab_app.views.handler500'
