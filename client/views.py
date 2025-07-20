from typing import Any
from django.db.models.query import QuerySet
#from django.shortcuts import render
from .models import Client
#from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView


class ClientListView(LoginRequiredMixin,ListView):
  template_name = 'client/client_list.html'
  model = Client
  context_object_name = 'clients'
  

  def get_queryset(self) -> QuerySet[Any]:
    return Client.objects.filter(user=self.request.user)


# Function based View for client list
"""@login_required
def client_list_view(request):
  clients = Client.objects.filter(user = request.user)
  template_name = 'client/client_list.html'
  context = {
    "clients":clients
  }
  return render(request,template_name,context)"""
