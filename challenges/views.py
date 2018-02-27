from django.shortcuts import render
from django.views import generic

from .models import Challenge


def index(request):
    challenges = Challenge.objects.all()
    return render(request, "challenges/index.html", {"challenges": challenges})


class DetailView(generic.DetailView):
    model = Challenge
    template_name = "challenges/detail.html"
