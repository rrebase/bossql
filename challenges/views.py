import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import DetailView, ListView

from .models import Challenge, ChallengeTopic


class IndexView(ListView):
    model = ChallengeTopic
    template_name = "challenges/index.html"
    context_object_name = "topics"


class DetailView(DetailView):
    model = Challenge
    template_name = "challenges/detail.html"
    context_object_name = "challenge"


class TopicDetailView(DetailView):
    model = ChallengeTopic
    template_name = "challenges/topic_detail.html"
    context_object_name = "topic"


class CheckAttemptEndpoint(View):
    def post(self, request, *args, **kwargs):
        params = json.loads(request.body.decode('UTF-8'))
        challenge = get_object_or_404(Challenge,
                                      pk=params.get("challengeId", None))
        return HttpResponse(json.dumps(
            challenge.attempt(params.get("attemptSql", None))
        ))
