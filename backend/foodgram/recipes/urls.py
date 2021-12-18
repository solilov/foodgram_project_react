from django.urls import include, path
from recipes.views import (FavoriteView, IngredientViewSet, RecipeViewSet,
                           TagViewSet)
from rest_framework.routers import DefaultRouter


app_name = 'recipes'

router = DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    path('recipes/<int:id>/favorite/',
         FavoriteView.as_view(),
         name='favorites'
         ),
]
