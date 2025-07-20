from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Client(models.Model):
  first_name = models.CharField(max_length=128)
  last_name = models.CharField(max_length=128)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients')

class ClientEmail(models.Model):
  email = models.EmailField(unique=True)
  client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='emails')

class ClientPhoneNumber(models.Model):
  phone_number = models.CharField(max_length=50)
  client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='phonenumbers')

