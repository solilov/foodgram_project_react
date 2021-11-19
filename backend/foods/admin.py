from django.contrib import admin

from foods.models import Amount, Ingredient, Recipe, Tag


admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(Amount)
