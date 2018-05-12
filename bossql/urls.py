"""bossql URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin, auth
from django.http import HttpResponse
from django.urls import include, path
from django.contrib.auth import views
import django.contrib.auth.urls

import challenges.views

urlpatterns = [
    path("", challenges.views.IndexView.as_view(), name="home"),
    path("accounts/", include("accounts.urls")),
    path("tutorials/", include("tutorials.urls")),
    path("stats/", include("stats.urls")),
    path("about/", include("about.urls")),
    path("challenges/", include("challenges.urls")),
    path("backdoor/", admin.site.urls),
    path('logout/', django.contrib.auth.views.LogoutView.as_view(), name='logout'),
    path('robots.txt', lambda x: HttpResponse("User-Agent: *\nDisallow:", content_type="text/plain"), name="robots_file"),
]
