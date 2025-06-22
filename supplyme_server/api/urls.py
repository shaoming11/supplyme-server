from django.urls import path
from . import views

urlpatterns = [
    path("", views.GetResults.as_view(), name="index")
]