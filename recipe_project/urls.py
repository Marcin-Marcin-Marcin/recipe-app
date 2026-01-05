from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import login_view, logout_view, success_view, about_view

urlpatterns = [
    path("admin/", admin.site.urls),

    # authentication
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("success/", success_view, name="success"),

    # about page
    path("about/", about_view, name="about"),

    # recipe app
    path("", include("recipes.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
