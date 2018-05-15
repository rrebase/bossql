from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailOrUsernameModelBackend(ModelBackend):
    """Allow authentication with either a username or an email address."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            if '@' in username:
                user = get_user_model().objects.get(email__iexact=username)
            else:
                user = get_user_model().objects.get(username__iexact=username)
            if user.check_password(password):
                return user
        except get_user_model().DoesNotExist:
            return None

    def get_user(self, username):
        try:
            return get_user_model().objects.get(pk=username)
        except get_user_model().DoesNotExist:
            return None
