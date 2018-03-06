import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import DetailView

from .models import Challenge


def index(request):
    challenges = Challenge.objects.all()
    return render(request, "challenges/index.html", {"challenges": challenges})


class DetailView(DetailView):
    model = Challenge
    template_name = "challenges/detail.html"
    context_object_name = "challenge"


class CheckAttemptEndpoint(View):
    def post(self, request, *args, **kwargs):
        params = json.loads(request.body.decode('UTF-8'))
        challenge = get_object_or_404(Challenge,
                                      pk=params.get("challengeId", None))
        return HttpResponse(json.dumps(
            challenge.attempt(params.get("attemptSql", None))
        ))
