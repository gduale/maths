from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include

urlpatterns = [
    path("connexion/", LoginView.as_view(
        template_name="practice/login.html", redirect_authenticated_user=True,
    ), name="login"),
    path("admin/", admin.site.urls),
    path("", include("practice.urls")),
]
