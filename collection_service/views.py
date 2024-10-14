from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Collection, Recipe, User

# Create your views here.

def get_collection(request, id):
    collection = get_object_or_404(Collection, id=id)
    return JsonResponse(collection_to_dict(collection))