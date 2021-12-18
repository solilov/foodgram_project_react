from django.contrib.auth import get_user_model
from django_filters import CharFilter, FilterSet, filters

from recipes.models import Ingredient, Recipe

User = get_user_model()


class TagOrAuthorFilter(FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    author = filters.ModelChoiceFilter(queryset=User.objects.all())

    class Meta:
        model = Recipe
        fields = ('tags', 'author')


class IngredientFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="startswith")

    class Meta:
        model = Ingredient
        fields = ("name",)
