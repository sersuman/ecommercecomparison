from django.db import models
from django.conf import settings
from django.utils import timezone


# Create your models here.
class Item(models.Model):
  name = models.CharField(max_length=200)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  created_date = models.DateTimeField(default=timezone.now)

  def __str__(self):
    return self.name