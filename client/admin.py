from django.contrib import admin
from .models import Client, ClientEmail, ClientPhoneNumber

admin.site.register(Client)
admin.site.register(ClientEmail)
admin.site.register(ClientPhoneNumber)
