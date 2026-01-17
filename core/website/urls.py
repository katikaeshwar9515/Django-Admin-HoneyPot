from django.urls import path,include
from . import views

app_name = "website"

urlpatterns = [
    path("", views.LandingView.as_view(), name="index"),
    path("upload/", views.UploadView.as_view(), name="upload"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("api/", include("website.api.urls")),
]