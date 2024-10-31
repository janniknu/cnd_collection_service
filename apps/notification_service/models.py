from django.db import models
from apps.collection_service.models import User

# Create your models here.

class Notification(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    message = models.TextField()