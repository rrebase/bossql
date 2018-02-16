from django.urls import path

from . import views

app_name = 'tutorials'
urlpatterns = [
    path("", views.index, name="index"),
]
