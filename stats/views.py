from django.shortcuts import render

from accounts.models import CustomUser


def index(request):
    order_by = request.GET.get("order_by", "-completed_challenges")
    users = CustomUser.objects.all().order_by(order_by)
    return render(request, "stats/index.html", {"users": users})
