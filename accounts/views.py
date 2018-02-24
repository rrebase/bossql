from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model, authenticate
from .forms import CustomUserCreationForm, CustomUserLoginForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView


class Login(LoginView):
    form_class = CustomUserLoginForm
    success_url = reverse_lazy("home")
    template_name = 'accounts/login.html'


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
