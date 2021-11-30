from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets

from rest_framework.response import Response
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

    # def add_obj(self, model, user, pk):
    #     """Добавить рецепт."""
    #     if model.objects.filter(user=user, recipe__id=pk).exists():
    #         return Response({
    #             'errors': 'Рецепт уже добавлен в список'
    #         }, status=status.HTTP_400_BAD_REQUEST)
    #     recipe = get_object_or_404(Recipe, id=pk)
    #     model.objects.create(user=user, recipe=recipe)
    #     serializer = RecipeSerializer(recipe)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
