from django.db import models
from client.models import Client


class JobCategory(models.Model):
  name = models.CharField(max_length=120)

class Job(models.Model):
  title = models.CharField(max_length=300)
  category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, related_name='jobs')
  