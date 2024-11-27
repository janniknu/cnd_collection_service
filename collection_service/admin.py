from django.contrib import admin
from .src.models import Collection, Recipe, User

# Register your models here.

admin.site.register(Collection)
admin.site.register(Recipe)
admin.site.register(User)
