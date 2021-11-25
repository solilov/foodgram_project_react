from django.urls import include, path

from foods.views import IngredientViewSet, RecipeViewSet, TagViewSet

from rest_framework.routers import DefaultRouter


app_name = 'foods'

router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
