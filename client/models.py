from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Client(models.Model):
  first_name = models.CharField(max_length=128)
  last_name = models.CharField(max_length=128)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients')

  def __str__(self) -> str:
      return f"{self.first_name} {self.last_name}"
  
  
class ClientEmail(models.Model):
    email = models.EmailField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='emails')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['client', 'email'], name='unique_email_per_client')
        ]


class ClientPhoneNumber(models.Model):
  phone_number = models.CharField(max_length=50)
  client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='phonenumbers')

  class Meta:
        constraints = [
            models.UniqueConstraint(fields=['client', 'phone_number'], name='unique_phone_number_per_client')
        ]

