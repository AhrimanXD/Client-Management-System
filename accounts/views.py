from django.forms import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from .forms import RegistrationForm
from django.views.generic import CreateView
from .models import User
from django.contrib.auth import login

class CustomLoginView(LoginView):
  template_name = "accounts/login.html"

class RegisterView(CreateView):
  template_name = 'accounts/register.html'
  form_class = RegistrationForm
  model = User
  success_url = reverse_lazy('client_list')

  def form_valid(self, form: BaseModelForm) -> HttpResponse:
    response = super().form_valid(form)

    user = form.instance
    login(self.request, user)

    return response
  
