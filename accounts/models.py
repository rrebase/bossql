from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(UserManager):
    pass


class MyValidator(UnicodeUsernameValidator):
    regex = r'^[\w.+-]+$'
    message = _(
        'Enter a valid username. This value may contain only letters, '
        'numbers, and ./+/-/_ characters.'
    )


class CustomUser(AbstractUser):
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and ./+/-/_ only.'),
        validators=[MyValidator()],
        error_messages={
            'unique': _('A user with that username already exists.'),
        },
    )
    email = models.EmailField('email address', blank=True, unique=True)
    completed_challenges = models.IntegerField(default=0)
    score = models.PositiveIntegerField(default=0)
    allow_seen_in_stats = models.BooleanField(default=True)
    is_email_public = models.BooleanField(default=False)

    objects = CustomUserManager()
