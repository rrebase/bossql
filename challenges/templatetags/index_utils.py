from django import template

from challenges.models import ChallengeTopic
from accounts.models import CustomUser

register = template.Library()


@register.filter
def get_solved_percent_for_user(topic: ChallengeTopic, user: CustomUser):
    if user.is_authenticated:
        counter = 0
        for challenge in topic.challenges.all():
            if challenge.attempts.filter(user=user):
                counter += 1 if challenge.attempts.filter(user=user).first().is_successful else 0
        return 0 if counter == 0 else counter / topic.challenges.count() * 100
    return 0
