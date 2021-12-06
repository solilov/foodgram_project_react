from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action

from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from rest_framework.viewsets import ReadOnlyModelViewSet

from api.pagination import RecipePagination
from api.serializers import CustomRecipeSerializer, IngredientSerializer, RecipeSerializer, TagSerializer

from recipes.models import Favorite, Ingredient, Recipe, Shopping_Cart, Tag


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

    @action(detail=True, methods=['get', 'delete'])
    def favorite(self, request, pk):
        if request.method == 'GET':
            recipe = get_object_or_404(Recipe, id=pk)
            Favorite.objects.get_or_create(
                user=self.request.user, recipe=recipe
            )
            serializer = CustomRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        Favorite.objects.filter(user=self.request.user, recipe_id=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get', 'delete'])
    def shopping_cart(self, request, pk):
        if request.method == 'GET':
            recipe = get_object_or_404(Recipe, id=pk)
            Shopping_Cart.objects.get_or_create(
                user=self.request.user,
                recipe=recipe
            )
            serializer = CustomRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        Shopping_Cart.objects.filter(
            user=self.request.user,
            recipe_id=pk
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # @action(detail=True, methods=['get'])
    # def download_shopping_cart(self):
    #     pass
