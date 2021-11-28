from django.contrib.auth import get_user_model

from djoser.serializers import UserCreateSerializer, UserSerializer

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from recipes.models import Tag


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
