from django.contrib import admin

from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag


class IngredientAdmin(admin.ModelAdmin):
    search_fields = ('name',)


class IngredientRecipeInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        IngredientRecipeInline,
    ]


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientRecipe)
