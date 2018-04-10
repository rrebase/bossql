from django.shortcuts import render
from django.views.generic import ListView

from accounts.models import CustomUser


class StatsView(ListView):
    model = CustomUser
    template_name = "stats/index.html"
    context_object_name = "users"


def index(request):
    order_by = request.GET.get("order_by", "-completed_challenges")
    users = CustomUser.objects.all().filter(allow_seen_in_stats=True).order_by(order_by)
    return render(request, "stats/index.html", {"users": users})
