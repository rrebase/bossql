from django.urls import path

from . import views


app_name = 'challenges'
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("check-attempt/", views.CheckAttemptEndpoint.as_view(), name="check_attempt"),
]
