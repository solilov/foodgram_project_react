from django.contrib import admin
from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            Shopping_Cart, Tag)


class IngredientAdmin(admin.ModelAdmin):
    search_fields = ('name',)


class IngredientRecipeInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        IngredientRecipeInline,
    ]
    list_display = ('author', 'name', 'favorite_count')
    list_filter = ('author', 'name', 'tags')

    def favorite_count(self, obj):
        return Favorite.objects.filter(recipe=obj).count()


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientRecipe)
admin.site.register(Favorite)
admin.site.register(Shopping_Cart)
