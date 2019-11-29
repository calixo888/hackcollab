from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "hackcollab_app"

urlpatterns = [
    path('admin/', admin.site.urls),
    url("^$", views.index, name="index"),
    url("^success", views.success, name="success"),
    url("^privacy-policy", views.privacy_policy, name="privacy_policy"),
    url("^terms-and-conditions", views.terms_and_conditions, name="terms_and_conditions"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'hackcollab_app.views.handler404'
handler500 = 'hackcollab_app.views.handler500'
