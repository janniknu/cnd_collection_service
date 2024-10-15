from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Collection, Recipe, User

# Create your views here.

def get_collection(request, id):
    collection = get_object_or_404(Collection, id=id)
    print("successfully")
    return JsonResponse(collection_to_dict(collection))


def create_collection(request):
    data = request.POST
    author = get_object_or_404(User, username=data['author'])
    collection = Collection.objects.create(
        id=data['id'],
        name=data['name'],
        author=author,
        description=data['description'],
        labels=data.get('labels', [])
    )
    return JsonResponse(collection_to_dict(collection))


def delete_collection(request, id):
    collection = get_object_or_404(Collection, id=id)
    collection.delete()
    # Trigger event
    trigger_event('collection_deleted', collection)
    return JsonResponse({'status': 'deleted'})






def collection_to_dict(collection):
    return {
        'id': collection.id,
        'name': collection.name,
        'author': collection.author.username,
        'description': collection.description,
        'recipes': [recipe.id for recipe in collection.recipes.all()],
        'labels': collection.labels
    }
    
def trigger_event(event_type, collection):
    # Implement event logic here
    print(f"Event triggered: {event_type} for collection {collection.id}")