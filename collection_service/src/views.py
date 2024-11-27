from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from .models import Collection, Recipe, User
from .rabbitmq_service import publishEvent
import json

# Create your views here.

invalid_json = "Invalid JSON"

@csrf_exempt
def collection_main(request, id=None):
    if request.method == 'GET':
        if id:
            return get_collection(id)
        else:
            return get_collections()
    elif request.method == 'POST':
        return create_collection(request)
    elif request.method == 'PUT':
        return update_collection(request, id)
    elif request.method == 'DELETE':
        return delete_collection(request,id)
    else:
        return HttpResponseBadRequest("Invalid request method")
    

@csrf_exempt 
def collection_edit_recipe(request, id):
    if request.method == 'POST':
        return collection_add_recipe(request, id)
    elif request.method == 'DELETE':
        return collection_remove_recipe(request, id)
    else:
        return HttpResponseBadRequest("Invalid request method")
    

def get_collection(id):
    collection = get_object_or_404(Collection, id=id)
    return JsonResponse(collection_to_dict(collection))


def get_collections():
    collections = Collection.objects.all()
    return JsonResponse([collection_to_dict(c) for c in collections], safe=False)


def create_collection(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest(invalid_json)
    author = get_object_or_404(User, username=data['author'])
    
    collection = Collection.objects.create(
        name=data['name'],
        author=author,
        description=data['description']
    )
    
    recipes = data.get('recipes', [])
    for recipe_id in recipes:
        recipe = get_object_or_404(Recipe, id=recipe_id)
        collection.recipes.add(recipe)
     
    # Trigger event
    publishEvent('collection.created', collection_to_dict(collection))
    return JsonResponse(collection_to_dict(collection))


def delete_collection(request, id):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest(invalid_json)
    
    collection = get_object_or_404(Collection, id=id)
    author = get_object_or_404(User, username=data['author'])   
    if author != collection.author:
        return HttpResponseForbidden("You are not authorized to delete this collection")
    
    # Trigger event
    publishEvent('collection.deleted', collection_to_dict(collection))
    collection.delete()
    return JsonResponse({'status': 'deleted'})



def update_collection(request, id):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest(invalid_json)
    
    collection = get_object_or_404(Collection, id=id)
    author = get_object_or_404(User, username=data['author'])   
    if author != collection.author:
        return HttpResponseForbidden("You are not authorized to update this collection")
    
    collection.name = data['name']
    collection.description = data['description']
    collection.recipes.clear()
    recipes = data.get('recipes', [])
    for recipe_id in recipes:
        recipe = get_object_or_404(Recipe, id=recipe_id)
        collection.recipes.add(recipe)
    
    collection.save()
    # Trigger event
    publishEvent('collection.updated', collection_to_dict(collection))
    return JsonResponse(collection_to_dict(collection))


def collection_add_recipe(request, id):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest(invalid_json)
    
    recipe_id = data.get('recipe_id')
    collection = get_object_or_404(Collection, id=id)
    recipe = get_object_or_404(Recipe, id=recipe_id)
    collection.recipes.add(recipe)
    return JsonResponse(collection_to_dict(collection))


def collection_remove_recipe(request, id):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest(invalid_json)
    
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
        'recipes': [recipe.id for recipe in collection.recipes.all()]
    }
    