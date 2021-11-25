from colorfield.fields import ColorField

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models


User = get_user_model()


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


class Ingredient(models.Model):
    """
    Модель ингридиента.
    """
    name = models.CharField(max_length=200,
                            verbose_name='название ингридиента')
    measurement_unit = models.CharField(max_length=20,
                                        verbose_name='единица измерения',
                                        help_text='Введите единицы измерения')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    """
    Модель рецепта.
    """
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipe',
                               verbose_name='автор рецепта')
    name = models.CharField(max_length=200, verbose_name='название рецепта')
    description = models.TextField(verbose_name='описание рецепта')
    image = models.ImageField(upload_to='recipe/',
                              verbose_name='картинка')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='Amount',
                                         verbose_name='ингредиенты')
    tags = models.ManyToManyField(Tag, verbose_name='тег')
    cooking_time = models.PositiveSmallIntegerField(
        help_text='время приготовления в минутах',
        verbose_name='время приготовления',
        validators=[MinValueValidator(1)]
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Amount(models.Model):
    """
    Модель количества ингридиента в рецепте.
    """
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   related_name='amount',
                                   verbose_name='ингредиент')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='amount',
                               verbose_name='рецепт')
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='количество ингредиента'
    )

    class Meta:
        ordering = ['-id']


class Favorites(models.Model):
    pass
