from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy
from django.views import generic

from accounts.forms import ChangeSettingsForm, CustomUserCreationForm, CustomUserLoginForm, PasswordChangeCustomForm
from accounts.models import CustomUser


class Login(LoginView):
    form_class = CustomUserLoginForm
    success_url = reverse_lazy('home')
    template_name = 'accounts/login.html'


class UserProfileView(generic.DetailView):
    model = CustomUser
    slug_field = 'username'
    template_name = 'accounts/profile.html'
    context_object_name = 'customuser'


class Register(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'accounts/register.html'

    def form_valid(self, form):
        valid = super(Register, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid


class PasswordChangeCustomView(PasswordChangeView):
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('accounts:password_change_done')
    form_class = PasswordChangeCustomForm


class PasswordChangeDoneCustomView(PasswordChangeDoneView):
    template_name = 'accounts/change_password_done.html'


class ChangeSettingsView(generic.UpdateView):
    template_name = 'accounts/change_settings.html'
    success_url = reverse_lazy('home')
    form_class = ChangeSettingsForm
    model = CustomUser

    def get_object(self, queryset=None):
        return self.request.user
