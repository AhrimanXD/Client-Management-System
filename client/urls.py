from django.urls import path
from .views import ClientListView,ClientDetailView,client_create_view

urlpatterns = [
  path('clients',ClientListView.as_view(),name='client_list'),
  path('clients/<int:pk>', ClientDetailView.as_view(), name='client_detail'),
  path('create-client', client_create_view, name='client_create')
]