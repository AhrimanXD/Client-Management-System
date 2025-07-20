from django.db import models
from client.models import Client
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


User = get_user_model()

class JobCategory(models.Model):
  name = models.CharField(max_length=120)

STATUS = [
  ('pending', 'Pending'),
  ('ongoing', 'Ongoing'),
  ('suspended', 'Suspended'),
  ('cancelled', 'Cancelled'),
  ('completed', 'Completed'),
  ('due', 'Due')
]
class Job(models.Model):
  title = models.CharField(max_length=300)
  description = models.TextField(max_length=1000, null=True, blank=True)
  category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, related_name='jobs')
  status = models.CharField(max_length=40, choices=STATUS)
  starting_date = models.DateField()
  due_date = models.DateField()
  price = models.DecimalField(max_digits=12, decimal_places=2)
  is_paid = models.BooleanField(default=False)
  client = models.ForeignKey(Client, related_name='jobs', on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')


  def clean(self):
        
        if self.starting_date > self.due_date:
            raise ValidationError("Starting date cannot be after due date.")

         # Ensure price is positive
        if self.price <= 0:
            raise ValidationError({'price': "Price must be a positive value."})

        if self.client.user != self.user:
            raise ValidationError("The client does not belong to the user assigning the job.")

  def save(self, *args, **kwargs):
    self.full_clean() 
    super().save(*args, **kwargs)