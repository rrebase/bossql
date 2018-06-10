from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm
from django.forms import ModelForm, CharField, PasswordInput

from accounts.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    error_messages = {
        'password_mismatch': 'The two password fields didn\'t match.',
    }

    password1 = CharField(
        label='Password',
        strip=False,
        widget=PasswordInput,
        help_text=None,
    )
    password2 = CharField(
        label='Password confirmation',
        widget=PasswordInput,
        strip=False,
        help_text='Enter the same password as before, for verification.',
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email',)
        help_texts = {
            'username': None,
            'email': 'We\'ll never share your email with anyone else.',
        }
        error_messages = ''

    def clean_username(self):
        if CustomUser.objects.filter(username__iexact=self.cleaned_data['username']):
            self.add_error('username', 'A user with that username already exists.')
        else:
            return self.cleaned_data['username']

    helper = FormHelper()
    helper.form_class = 'form-group'
    helper.layout = Layout(
        Field('username', css_class='form-control', autocomplete='username'),
        Field('email', css_class='form-control', autocomplete='email'),
        Field('password1', css_class='form-control', autocomplete='off'),
        Field('password2', css_class='form-control', autocomplete='off'),
        Submit('Sign up', 'Sign up', css_class='mt-2', css_id='sign_up'),
    )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields


class CustomUserLoginForm(AuthenticationForm):

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields['username'].label = 'Username or Email'

    error_messages = {
        'invalid_login': "Please enter a correct %(username)s and password.",
        'inactive': "This account is inactive.",
    }

    helper = FormHelper()
    helper.form_class = 'form-group'
    helper.layout = Layout(
        Field('username', css_class='form-control', autocomplete='username'),
        Field('password', css_class='form-control', autocomplete='current-password'),
        Submit('Log in', 'Log in', css_class='mt-2', css_id='log_in'),
    )


class ChangeSettingsForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['allow_seen_in_stats'].widget.attrs['class'] = 'form-check-input'

    class Meta:
        model = CustomUser
        fields = ('allow_seen_in_stats', 'line_numbers')

    helper = FormHelper()
    helper.form_class = 'form-group'
    helper.layout = Layout(
        Field('allow_seen_in_stats', css_class='form-check', autocomplete='off'),
        Field('line_numbers', css_class='form-check', autocomplete='off'),
        Submit('Save settings', 'Save settings', css_class='mt-2', css_id='save_settings'),
    )


class PasswordChangeCustomForm(PasswordChangeForm):
    new_password1 = CharField(
        label="New password",
        widget=PasswordInput,
        strip=False,
        help_text=None,
    )

    helper = FormHelper()
    helper.form_class = 'form-group'
    helper.layout = Layout(
        Field('old_password', css_class='form-control', autocomplete='current-password'),
        Field('new_password1', css_class='form-control', autocomplete='off'),
        Field('new_password2', css_class='form-control', autocomplete='off'),
        Submit('Change my password', 'Change my password', css_class='mt-2', css_id='change_pw'),
    )
