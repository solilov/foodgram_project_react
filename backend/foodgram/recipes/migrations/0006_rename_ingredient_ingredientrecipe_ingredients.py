# Generated by Django 3.2.9 on 2021-11-28 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_rename_ingredient_recipe_ingredients'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredientrecipe',
            old_name='ingredient',
            new_name='ingredients',
        ),
    ]
