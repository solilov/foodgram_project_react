from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from rest_framework.viewsets import ReadOnlyModelViewSet

from api.pagination import RecipePagination
from api.serializers import IngredientSerializer ,RecipeSerializer, TagSerializer

from recipes.models import Ingredient, Recipe, Tag


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['name', 'slug', 'id']


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['name', 'id']


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['name', 'id']
    pagination_class = RecipePagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
