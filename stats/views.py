import re

from django.shortcuts import render
from django.views.generic import ListView

from accounts.models import CustomUser


class StatsView(ListView):
    model = CustomUser
    template_name = "stats/index.html"
    context_object_name = "users"

    def get_ordering(self):
        order_by = self.request.GET.get("order_by", "")
        if not re.match("^-?(username|completed_challenges|score)$", order_by):
            return "-score"
        else:
            return order_by

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["order_by"] = self.get_ordering()
        return context_data

    def get_queryset(self):
        return super().get_queryset().filter(allow_seen_in_stats=True)
