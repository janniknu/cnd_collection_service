"""
URL configuration for recipe_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from collection_service import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('collections/', views.get_collections, name='get_collections'),
    path('collections/create/', views.create_collection, name='create_collection'),
    path('collections/<str:id>/', views.get_collection, name='get_collection'), 
    path('collections/<str:id>/update/', views.update_collection, name='update_collection'),
    path('collections/<str:id>/delete/', views.delete_collection, name='delete_collection'),
    path('collections/<str:id>/add_recipe/', views.add_recipe, name='add_recipe'),
    path('collections/<str:id>/remove_recipe/', views.remove_recipe, name='remove_recipe'),
]
