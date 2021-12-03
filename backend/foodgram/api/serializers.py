from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from recipes.models import Favorite, Ingredient, IngredientRecipe, Recipe , Tag
from users.models import Follow


User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    """
    Сериализатор модели User, для создания пользователя.
    """
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
    name = serializers.StringRelatedField(source='ingredient.name')
    measurement_unit = serializers.StringRelatedField(
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
    author = CustomUserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            # 'image'
            'text',
            'cooking_time'
        ]

    def validate(self, data):
        tags = self.initial_data.get("tags")
        if not tags:
            raise serializers.ValidationError("Обязательно нужно выбрать тег")
        data["tags"] = tags
        ingredients = self.initial_data.get("ingredients")
        if not ingredients or len(ingredients) < 1:
            raise serializers.ValidationError(
                "Поле ингредиент не может быть пустым"
            )
        data["ingredients"] = ingredients
        return data

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients:
            IngredientRecipe.objects.create(
                recipe=recipe,
                ingredient_id=ingredient.get("id"),
                amount=ingredient.get("amount"),
            )
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        instance.ingredients.clear()
        for ingredient in ingredients:
            IngredientRecipe.objects.create(
                recipe=instance,
                ingredient_id=ingredient.get("id"),
                amount=ingredient.get("amount"),
            )
        instance.tags.set(tags)
        return super().update(instance, validated_data)

    def get_is_favorited(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        return Recipe.objects.filter(favorites__user=user, id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        return Recipe.objects.filter(
            shopping_cart__user=user, id=obj.id
        ).exists()


class FollowSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Follow.
    """

    email = serializers.EmailField(read_only=True, source='following.email')
    id = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='following.id'
    )
    username = serializers.CharField(
        read_only=True,
        source='following.username'
    )
    first_name = serializers.CharField(
        read_only=True,
        source='following.first_name'
    )
    last_name = serializers.CharField(
        read_only=True,
        source='following.last_name'
    )
    is_subscribed = serializers.SerializerMethodField()
    # recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(
        source="following.recipes.count", read_only=True)

    class Meta:
        model = Follow
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            # 'recipes',
            'recipes_count'
        ]

    def get_is_subscribed(self, obj):
        obj.user.follower.filter(following=obj.following).exists()


class CustomRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор выдает только необходимые поля модели Recipe.
    """
    # image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'cooking_time']
        read_only_fields = ['id', 'name', 'cooking_time']