from django.urls import path, re_path
from django.views.generic import RedirectView

from accounts import views

app_name = 'accounts'
urlpatterns = [
    path('', RedirectView.as_view(pattern_name='home', permanent=False)),
    path('password_change/', views.PasswordChangeCustomView.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDoneCustomView.as_view(), name='password_change_done'),
    path('change_settings/', views.ChangeSettingsView.as_view(), name='change_settings'),
    re_path(r'^(?P<slug>[\w.+-]+)/$', views.UserProfileView.as_view(), name='profile'),
]
