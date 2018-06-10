import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import DetailView, ListView

from accounts.models import CustomUser
from challenges.models import Challenge, ChallengeTopic


class AdminTopicSourceTablesView(DetailView):
    model = ChallengeTopic
    template_name = 'challenges/_admin_topic_source_tables.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tables'] = self.get_object().source_tables.all()
        return context


class IndexView(ListView):
    model = ChallengeTopic
    template_name = 'challenges/index.html'
    context_object_name = 'topics'


@method_decorator(ensure_csrf_cookie, name='dispatch')
class TopicDetailView(DetailView):
    model = ChallengeTopic
    template_name = 'challenges/topic_detail.html'
    context_object_name = 'topic'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if isinstance(self.request.user, CustomUser):
            line_numbers = self.request.user.line_numbers
        else:
            line_numbers = True
        context['django_data'] = json.dumps({'line_numbers': line_numbers})
        return context


class CheckAttemptEndpoint(View):

    def post(self, request, *args, **kwargs):
        params = json.loads(request.body.decode('UTF-8'))
        challenge = get_object_or_404(Challenge,
                                      pk=params.get('challengeId', None))
        return HttpResponse(json.dumps(
            challenge.attempt(params.get('attemptSql', None), self.request.user)
        ))
