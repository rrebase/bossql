from django.urls import path, re_path
from . import views

app_name = "accounts"
urlpatterns = [
    path("login", views.Login.as_view(), name="login"),
    path("register", views.Register.as_view(), name="register"),
    # path("<int:pk>/", views.Profile.as_view(), name="profile"),  # this is currently more reliable
    re_path(r'^(?P<username>\w+)/$', views.profile_view, name="profile"),  # case sensitive?
]
