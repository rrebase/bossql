from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Challenge


def index(request):
    challenges = Challenge.objects.all()
    return render(request, "challenges/index.html", {"challenges": challenges})


def detail(request, challenge_id):
    challenge = get_object_or_404(Challenge, pk=challenge_id)
    return render(request, "challenges/detail.html", {"challenge": challenge})
