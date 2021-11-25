from re import search
from django.contrib import admin

from foods.models import Amount, Ingredient, Recipe, Tag


class AmountInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        AmountInline,
    ]


class IngredientAdmin(admin.ModelAdmin):
    search_fields = ('name',)


admin.site.register(Tag)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Amount)
