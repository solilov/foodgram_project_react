from colorfield.fields import ColorField

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.deletion import CASCADE


User = get_user_model()


class Tag(models.Model):
    """
    Модель тега.
    """
    title = models.CharField(max_length=200,
                             unique=True,
                             verbose_name='название тега')
    color = ColorField(default='#FF0000')
    slug = models.SlugField(verbose_name='Слаг', unique=True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Тег'

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    """
    Модель ингридиента.
    """
    title = models.CharField(max_length=200,
                             unique=True,
                             verbose_name='название ингридиента')
    unit = models.CharField(max_length=20,
                            verbose_name='единица измерения',
                            help_text='Введите единицы измерения')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Ингридиент'

    def __str__(self):
        return self.title


class Recipe(models.Model):
    """
    Модель рецепта.
    """
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipe',
                               verbose_name='автор рецепта')
    title = models.CharField(max_length=200, verbose_name='название рецепта')
    description = models.TextField(verbose_name='описание рецепта')
    image = models.ImageField(upload_to='recipe/',
                              verbose_name='картинка')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='Amount',
                                         verbose_name='ингредиенты')
    tag = models.ManyToManyField(Tag, verbose_name='тег')
    cooking_time = models.PositiveSmallIntegerField(
        help_text='время приготовления в минутах',
        verbose_name='время приготовления',
        validators=[MinValueValidator(1)]
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'

    def __str__(self):
        return self.title


class Amount(models.Model):
    """
    Модель количества ингридиента в рецепте.
    """
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   verbose_name='ингредиент')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name='рецепт')
    amount_ingredient = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='количество ингредиента'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Количество ингредиента'

    def __str__(self):
        return self.amount_ingredient
