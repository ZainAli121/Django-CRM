from django.db import models
from datetime import datetime

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.username