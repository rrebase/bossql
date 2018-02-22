from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm

AUTH_USER_MODEL = "accounts.CustomUser"

def login(request):
    return render(request, "accounts/login.html", {})


class Register(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("home")
    template_name = "accounts/register.html"


def register(request):
    return render(request, "accounts/register.html", {})
