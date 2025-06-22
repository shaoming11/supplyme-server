from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api", views.GetResults.as_view(), name="api")
]