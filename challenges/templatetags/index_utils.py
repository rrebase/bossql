from django import template

from challenges.models import ChallengeTopic
from accounts.models import CustomUser

register = template.Library()


@register.filter
def get_solved_percent_for_user(topic: ChallengeTopic, user: CustomUser):
    if user.is_authenticated:
        counter = user.challenge_attempts.filter(challenge__topic=topic, is_successful=True).count()
        return 0 if counter == 0 else counter / topic.challenges.count() * 100
    return 0
