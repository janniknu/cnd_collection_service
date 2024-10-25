from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=100)

class Recipe(models.Model):
    name = models.CharField(max_length=100)

class Collection(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    recipes = models.ManyToManyField(Recipe)
    #labels = models.JSONField(default=list)