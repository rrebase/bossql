from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from accounts.models import CustomUser
from .forms import ChangeSettingsForm, CustomUserCreationForm, CustomUserLoginForm, PasswordChangeCustomForm


class Login(LoginView):
    form_class = CustomUserLoginForm
    success_url = reverse_lazy("home")
    template_name = 'accounts/login.html'


def profile_view(request, username):
    # TODO: clean up and show success message
    try:
        instance = CustomUser.objects.get(id=request.user.id)
    except CustomUser.DoesNotExist:
        return render(request, "accounts/profile.html", {"customuser": CustomUser.objects.get(username=username)})
    form = ChangeSettingsForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        messages.success(request, 'Profile details updated.')
        return HttpResponseRedirect(request.path_info)
    context = {"customuser": CustomUser.objects.get(username=username), "form": form}
    return render(request, "accounts/profile.html", context)


# class Profile(generic.DetailView):
#     model = CustomUser
#     template_name = "accounts/profile.html"


class Register(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("home")
    template_name = "accounts/register.html"

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
