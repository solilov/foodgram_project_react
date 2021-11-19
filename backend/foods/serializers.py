from rest_framework import serializers

from .models import Ingredient, Tag


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Тег.
    """

    class Meta:
        model = Tag
        fields = ('id', 'title', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Ингредиент.
    """

    class Meta:
        model = Ingredient
        fields = ('id', 'title', 'unit')
