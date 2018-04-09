from django import template

register = template.Library()

@register.filter
def get_attempt_for_user(challenge, user):
    return challenge.attempts.filter(user=user).first()