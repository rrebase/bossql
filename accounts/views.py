from django.shortcuts import render
from django.http import HttpResponseRedirect


def login(request):
    return render(request, "accounts/login.html", {})


def register(request):
    return render(request, "accounts/register.html", {})