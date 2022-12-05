""".
URL mappings for the recipe app.
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter
# You can use routers with an API view to automatically create
# routes for all the available options for that view.

from recipe import views


router = DefaultRouter()
router.register('recipes', views.RecipeViewSet)
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)
# router.register('recipes', views)
# creates a new endpoint api/recipes/ and it will asign all the
# different endpoints from our viewset to that endpoint.
# The recipe viewset is gonna have auto generated urls depending
# on the functionality that's enabled on the viewset.
# Because we're using the Model Viewset, it will support all CRUD methods.

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]
