from django.urls import path, re_path
from django.views.generic import RedirectView

from . import views

app_name = "accounts"
urlpatterns = [
    path("", RedirectView.as_view(pattern_name='home', permanent=False)),
    path("login", views.Login.as_view(), name="login"),
    path("register", views.Register.as_view(), name="register"),
    path('password_change/', views.PasswordChangeCustomView.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDoneCustomView.as_view(), name='password_change_done'),
    path('change_settings', views.ChangeSettingsView.as_view(), name='change_settings'),
    re_path(r'^(?P<username>\w+)/$', views.profile_view, name="profile"),
]
