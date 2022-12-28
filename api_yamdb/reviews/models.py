from django.db import models
# валидаторы добавим позже


class Category(models.Model):
    """Класс категорий."""
    name = models.CharField(
        max_length=200,
    )
    slug = models.SlugField(
        max_length=70,
        unique=True,
    )


class Genre(models.Model):
    """Класс жанров."""
    name = models.CharField(
        max_length=200,
    )
    slug = models.SlugField(
        max_length=70,
        unique=True,
    )


class Title(models.Model):
    """Класс произведений."""

    name = models.CharField(
        max_length=150,

    )
    year = models.PositiveIntegerField()

    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles',
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )


class GenreTitle(models.Model):
    """Kласс, связывающий жанры и произведения."""
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )
