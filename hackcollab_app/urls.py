from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views

app_name = "hackcollab_app"

urlpatterns = [
    path('admin/', admin.site.urls),
    url("^$", views.index, name="index"),
]
