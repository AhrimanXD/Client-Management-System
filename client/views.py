from typing import Any
from django.db.models.query import QuerySet
#from django.shortcuts import render
from .models import Client
#from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView


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

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    client = self.get_object()
    context['emails'] = client.emails.all()
    context['phone_numbers'] = client.phonenumbers.all()
    return context

# Function based View for client list
"""@login_required
def client_list_view(request):
  clients = Client.objects.filter(user = request.user)
  template_name = 'client/client_list.html'
  context = {
    "clients":clients
  }
  return render(request,template_name,context)"""
