from django import template

from challenges.models import ChallengeAttempt

register = template.Library()

@register.filter
def get_attempt_for_user(challenge, user):
    if user.is_authenticated:
        return challenge.attempts.filter(user=user).first()
    else:
        return ChallengeAttempt.objects.none()