from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Collection, Recipe, User
from .rabbitmq_service import publishEvent
import json

# Create your views here.

#def collection_main(request):
def get_collection(request, id):
    collection = get_object_or_404(Collection, id=id)
    publishEvent('get')
    return JsonResponse(collection_to_dict(collection))


#ist das korrekt so? Alle oder nur ausgewählte?
def get_collections(request):
    collections = Collection.objects.all()
    return JsonResponse([collection_to_dict(c) for c in collections], safe=False)


@csrf_exempt
def create_collection(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Only POST requests are allowed")
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")
    
    author = get_object_or_404(User, username=data['author'])
    collection = Collection.objects.create(
        id=data['id'],
        name=data['name'],
        author=author,
        description=data['description'],
        labels=data.get('labels', [])
    )
    
    recipes = data.get('recipes', [])
    for recipe_id in recipes:
        recipe = get_object_or_404(Recipe, id=recipe_id)
        collection.recipes.add(recipe)
     
    # Trigger event
    trigger_event('created', collection.id)
    return JsonResponse(collection_to_dict(collection))


def delete_collection(request, id):
    collection = get_object_or_404(Collection, id=id)
    deleted_id = collection.id
    collection.delete()
    # Trigger event
    trigger_event('deleted', deleted_id)
    return JsonResponse({'status': 'deleted'})

#author update zulassen? Aktuell wird der username des updaters reingenommen
@csrf_exempt
def update_collection(request, id):
    if request.method != 'POST':
        return HttpResponseBadRequest("Only POST requests are allowed")
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")
    
    collection = get_object_or_404(Collection, id=id)
    collection.name = data['name']
    collection.description = data['description']
    collection.labels = data.get('labels', [])
    collection.recipes.clear()
    recipes = data.get('recipes', [])
    for recipe_id in recipes:
        recipe = get_object_or_404(Recipe, id=recipe_id)
        collection.recipes.add(recipe)
    
    collection.save()
    # Trigger event
    trigger_event('updated', collection.id)
    return JsonResponse(collection_to_dict(collection))


@csrf_exempt
def add_recipe(request, id):
    if request.method != 'POST':
        return HttpResponseBadRequest("Only POST requests are allowed")
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")
    
    recipe_id = data.get('recipe_id')
    collection = get_object_or_404(Collection, id=id)
    recipe = get_object_or_404(Recipe, id=recipe_id)
    collection.recipes.add(recipe)
    return JsonResponse(collection_to_dict(collection))


@csrf_exempt
def remove_recipe(request, id):
    if request.method != 'POST':
        return HttpResponseBadRequest("Only POST requests are allowed")
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")
    
    recipe_id = data.get('recipe_id')
    collection = get_object_or_404(Collection, id=id)
    recipe = get_object_or_404(Recipe, id=recipe_id)
    collection.recipes.remove(recipe)
    return JsonResponse(collection_to_dict(collection))


def collection_to_dict(collection):
    return {
        'id': collection.id,
        'name': collection.name,
        'author': collection.author.username,
        'description': collection.description,
        'recipes': [recipe.id for recipe in collection.recipes.all()],
        'labels': collection.labels
    }
    
def trigger_event(event_type, collection_id):
    # Implement event logic here
    print(f"Event triggered: collection {collection_id} was {event_type}")