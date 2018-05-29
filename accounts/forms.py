from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm
from django.forms import ModelForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for field in ("username", "email", "password1", "password2"):
            if field in self.fields:
                self.fields[field].widget.attrs["class"] = "form-control"

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email")
        error_messages = ""

    def clean_username(self):
        if CustomUser.objects.filter(username__iexact=self.cleaned_data['username']):
            self.add_error('username', 'A user with that username already exists.')
        else:
            return self.cleaned_data['username']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields


class CustomUserLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["password"].widget.attrs["class"] = "form-control"


class ChangeSettingsForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields["allow_seen_in_stats"].widget.attrs["class"] = "form-check-input"

    class Meta:
        model = CustomUser
        fields = ("allow_seen_in_stats",)


class PasswordChangeCustomForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget.attrs["class"] = "form-control"
        self.fields["new_password1"].widget.attrs["class"] = "form-control"
        self.fields["new_password2"].widget.attrs["class"] = "form-control"
