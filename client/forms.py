from .models import Client,ClientEmail,ClientPhoneNumber
from django.forms import ModelForm


class ClientCreationForm(ModelForm):
  class Meta:
    model = Client
    fields = ['first_name', 'last_name']

class ClientEmailForm(ModelForm):
  class Meta:
    model = ClientEmail
    fields = ['email']

class ClientPhoneNumberForm(ModelForm):
  class Meta:
    model = ClientPhoneNumber
    fields = ['phone_number']