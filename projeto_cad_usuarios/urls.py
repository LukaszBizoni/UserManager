"""URL configuration for projeto_cad_usuarios project."""

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("app_cad_usuarios.urls")),
]
