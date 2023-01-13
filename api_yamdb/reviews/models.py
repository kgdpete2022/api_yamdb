from datetime import date

from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models

from users.models import User


class Category(models.Model):

    name = models.CharField(max_length=256,
                            verbose_name='Категория',)
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[RegexValidator(regex=r'^[-a-zA-Z0-9_]+$')],
        verbose_name='URL'
    )

    def __str__(self):
        return self.name


class Genre(models.Model):

    name = models.CharField(max_length=50,
                            verbose_name='Жанр', )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[RegexValidator(regex=r'^[-a-zA-Z0-9_]+$')],
        verbose_name='URL'
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=128,
                            verbose_name='Название',
                            )
    year = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(date.today().year),
            MinValueValidator(1)
        ],
        verbose_name='Дата выхода',
    )
    description = models.TextField(
        max_length=256,
        verbose_name='Описание',
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='genres',
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        default='Категория не определена',
        on_delete=models.SET_DEFAULT,
        related_name='titles',
    )

    class Meta:
        ordering = ('year',)

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews',
        db_column='title_id',

    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка')
    pub_date = models.DateTimeField(
        'pub_date',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]

    def __str__(self):
        return self.text


class Comments(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Дата публикации',
        related_name='comments',
        on_delete=models.CASCADE,
        db_column='review_id'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='author',
    )
    pub_date = models.DateTimeField(
        'pub_date',
        auto_now_add=True,
    )

    def __str__(self):
        return self.text
