from django.contrib import admin
from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            Shopping_Cart, Tag)


class IngredientAdmin(admin.ModelAdmin):
    search_fields = ('name',)


class IngredientRecipeInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    search_fields = ['name', 'author', 'tags']
    inlines = [
        IngredientRecipeInline,
    ]


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientRecipe)
admin.site.register(Favorite)
admin.site.register(Shopping_Cart)
