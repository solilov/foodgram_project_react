from api.filters import IngredientFilter, TagOrAuthorFilter
from api.pagination import CustomPagination
from api.serializers import (CustomRecipeSerializer, IngredientSerializer,
                             RecipeSerializer, TagSerializer)
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            Shopping_Cart, Tag)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['name', 'slug', 'id']


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = TagOrAuthorFilter
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.query_params.get('is_favorited'):
            return Recipe.objects.filter(favorites__user=self.request.user)
        elif self.request.query_params.get('is_in_shopping_cart'):
            return Recipe.objects.filter(shopping_cart__user=self.request.user)
        return Recipe.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'])
    def download_shopping_cart(self, request):
        user = request.user
        shopping_list = IngredientRecipe.objects.filter(
            recipe__shopping_cart__user=user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount')).order_by()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = (
            'attachment; filename="shopping_list.pdf"'
        )
        pdfmetrics.registerFont(TTFont('Petersburg', 'PetersburgITT.ttf'))
        p = canvas.Canvas(response)
        p.setFont('Petersburg', 24)
        p.drawString(200, 800, 'Список покупок')
        p.setFont('Petersburg', 20)
        number = 1
        height = 750
        for i in shopping_list:
            p.drawString(100, height, text=(
                f'{number}) {i["ingredient__name"]} - {i["amount"]}'
                f'{i["ingredient__measurement_unit"]}'
            ))
            height -= 20
            number += 1
        p.showPage()
        p.save()
        return response

    @action(detail=True, methods=['get', 'delete'])
    def shopping_cart(self, request, pk):
        if request.method == 'GET':
            recipe = get_object_or_404(Recipe, id=pk)
            Shopping_Cart.objects.create(
                user=request.user,
                recipe=recipe
            )
            serializer = CustomRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        Shopping_Cart.objects.filter(
            user=self.request.user,
            recipe_id=pk
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        Favorite.objects.get_or_create(
            user=self.request.user, recipe=recipe
        )
        serializer = CustomRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        Favorite.objects.filter(user=self.request.user, recipe_id=id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
