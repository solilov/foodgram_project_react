from colorfield.fields import ColorField

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.deletion import CASCADE


User = get_user_model()


class Ingredient(models.Model):
    """
    Модель ингредиента.
    """
    name = models.CharField(
        max_length=256,
        verbose_name='название ингридиента'
    )
    measurement_unit = models.CharField(
        max_length=64,
        verbose_name='единица измерения',
        help_text='Введите единицы измерения'
    )

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'


class Tag(models.Model):
    """
    Модель тега.
    """
    name = models.CharField(max_length=200,
                            unique=True,
                            verbose_name='название тега')
    color = ColorField(default='#FF0000')
    slug = models.SlugField(verbose_name='Слаг', unique=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """
    Модель рецепта.
    """
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='автор рецепта')
    image = models.ImageField(upload_to='recipes/images',
                              verbose_name='картинка')
    name = models.CharField(max_length=256,
                            unique=True,
                            verbose_name='название рецепта')
    text = models.TextField(verbose_name='описание рецепта')
    tags = models.ManyToManyField(Tag, verbose_name='тег')
    cooking_time = models.PositiveSmallIntegerField(
        help_text='время приготовления в минутах',
        verbose_name='время приготовления',
        validators=[MinValueValidator(1)]
    )
    ingredients = models.ManyToManyField(Ingredient,
                                         through='IngredientRecipe')

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    """
    Модель отдельного ингредиента в рецепте с количеством.
    """
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=CASCADE,
        related_name='ingredient_recipe',
        verbose_name='ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=CASCADE,
        related_name='ingredient_recipe',
        verbose_name='рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='количество ингредиента'
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'Ингредиенты для рецепта {self.recipe}'


class Favorite(models.Model):
    """
    Модель для избранных рецептов.
    """
    user = models.ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=CASCADE,
        related_name='favorites',
        verbose_name='рецепт'
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_favorite')
        ]

    def __str__(self):
        return self.recipe.name


class Shopping_Cart(models.Model):
    """
    Модель корзины покупок.
    """
    user = models.ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='shopping_cart'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=CASCADE,
        related_name='shopping_cart',
        verbose_name='рецепт'
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_shopping_cart')
        ]

    def __str__(self):
        return self.recipe.name
