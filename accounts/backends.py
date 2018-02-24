from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
UserModel = get_user_model()


class EmailOrUsernameModelBackend(ModelBackend):
    """Allow authentication with either a username or an email address."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = UserModel.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None

    def get_user(self, username):
        try:
            return UserModel.objects.get(pk=username)
        except UserModel.DoesNotExist:
            return None
