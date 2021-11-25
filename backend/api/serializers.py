from drf_extra_fields.fields import Base64ImageField

from rest_framework import serializers

from foods.models import Amount, Ingredient, Recipe, Tag


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Тег.
    """

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Ингредиент.
    """

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class AmountSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Количество.
    """

    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )
    id = serializers.ReadOnlyField(source='ingredient.id')

    class Meta:
        model = Amount
        fields = ['id', 'name', 'measurement_unit', 'amount']


class RecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Рецепт.
    """
    tags = TagSerializer(many=True, read_only=True)
    author = serializers.StringRelatedField(read_only=True)  # здесь нужен кастомный сериализатор
    ingredients = AmountSerializer(many=True, read_only=True,
                                   source='amount')
    is_favorited = serializers.BooleanField(read_only=True) # не отображается       
    is_in_shopping_cart = serializers.BooleanField(read_only=True) # не отображается
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'description',
                  'cooking_time')
