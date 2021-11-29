from django.contrib.auth import get_user_model

from djoser.serializers import UserCreateSerializer, UserSerializer

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from recipes.models import Ingredient, IngredientRecipe, Recipe ,Tag


User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор модели User, для создания пользователя."""
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email',
                  'password')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'username': {'required': True},
            'email': {'required': True},
            'password': {'required': True},

        }


class CustomUserSerializer(UserSerializer):
    """
    Сериализатор модели User для отображения профиля пользователя,
    списка пользователей.
    """
    # is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id',  'username', 'first_name', 'last_name',
                  )


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Tag.
    """
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class IngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Ingredient.
    """
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели IngredientRecipe.
    Для отображения конкретных данных по ингредиенту.
    """
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )
    id = serializers.ReadOnlyField(source='ingredient.id')

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Рецепт.
    """
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientRecipeSerializer(many=True,
                                             read_only=True,
                                             source='ingredient_recipe')

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'text', 'tags', 'cooking_time', 'ingredients']
