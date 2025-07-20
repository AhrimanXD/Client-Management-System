from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpResponse,HttpRequest,Http404
from django.shortcuts import render, redirect
from .models import Client,ClientEmail,ClientPhoneNumber
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView,CreateView,UpdateView
from .forms import *
from django.forms.models import inlineformset_factory

EmailFormSet = inlineformset_factory(Client, ClientEmail, fields=['email'], extra=1, can_delete=True)
PhoneFormSet = inlineformset_factory(Client, ClientPhoneNumber, fields=['phone_number'], extra = 1, can_delete=True)
class ClientListView(LoginRequiredMixin,ListView):
  template_name = 'client/client_list.html'
  model = Client
  context_object_name = 'clients'
  

  def get_queryset(self) -> QuerySet[Any]:
    return Client.objects.filter(user=self.request.user)

class ClientDetailView(LoginRequiredMixin, DetailView):
  template_name = "client/client_detail.html"
  model = Client
  context_object_name = 'client'
  def get_object(self, queryset=None) -> Model:
    obj = super().get_object(queryset)
    if obj.user != self.request.user:
      raise Http404("You do not have permission to view this client.")
    return obj
  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    client = self.get_object()
    context['emails'] = client.emails.all()
    context['phone_numbers'] = client.phonenumbers.all()
    return context

@login_required
def client_create_view(request:HttpRequest)->HttpResponse:
  if request.method == 'POST':
    client_form = ClientCreationForm(request.POST)
    email_form = ClientEmailForm(request.POST)
    phone_form = ClientPhoneNumberForm(request.POST)

    if client_form.is_valid():
      client = client_form.save(commit=False)
      client.user = request.user
      client.save()

      if email_form.is_valid() and email_form.cleaned_data.get('email'):
        email = email_form.save(commit=False)
        email.client = client
        email.save()

            
      if phone_form.is_valid() and phone_form.cleaned_data.get('phone_number'):
        phone = phone_form.save(commit=False)
        phone.client = client
        phone.save()

      return  redirect('client_detail', pk = client.id)
  else:
    client_form = ClientCreationForm()
    email_form = ClientEmailForm()
    phone_form = ClientPhoneNumberForm()

  return render(request, template_name='client/client_create.html', context = {
      "client_form":client_form, "email_form":email_form, "phone_form": phone_form
    })

class ClientUpdateView(LoginRequiredMixin, UpdateView):
  model = Client
  fields = ['first_name','last_name']
  template_name = "client/client_update.html"

  def get_object(self, queryset=None) -> Model:
    obj = super().get_object(queryset)
    if obj.user != self.request.user:
      raise Http404("You do not have permission to edit this client")
    return obj
  def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['email_formset'] = EmailFormSet(self.request.POST, instance=self.object)
            context['phone_formset'] = PhoneFormSet(self.request.POST, instance=self.object)
        else:
            context['email_formset'] = EmailFormSet(instance=self.object)
            context['phone_formset'] = PhoneFormSet(instance=self.object)
        return context
  def form_valid(self, form):
        context = self.get_context_data()
        email_formset = context['email_formset']
        phone_formset = context['phone_formset']

        if email_formset.is_valid() and phone_formset.is_valid():
            self.object = form.save()
            email_formset.instance = self.object
            phone_formset.instance = self.object
            email_formset.save()
            phone_formset.save()
            return redirect(self.object.get_absolute_url())  # or whatever URL you use
        else:
            return self.render_to_response(self.get_context_data(form=form))


# Function based View for client list
"""@login_required
def client_list_view(request):
  clients = Client.objects.filter(user = request.user)
  template_name = 'client/client_list.html'
  context = {
    "clients":clients
  }
  return render(request,template_name,context)"""
