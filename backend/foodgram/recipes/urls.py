from django.urls import include, path

from recipes.views import IngredientViewSet, TagViewSet

from rest_framework.routers import DefaultRouter


app_name = 'recipes'

router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
