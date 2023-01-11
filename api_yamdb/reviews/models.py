from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, MinValueValidator


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


class User(AbstractUser):
    ROLE_USER = 'user'
    ROLE_MODERATOR = 'moderator'
    ROLE_ADMIN = 'admin'

    ROLES = (
        (ROLE_USER, 'Пользователь'),
        (ROLE_MODERATOR, 'Модератор'),
        (ROLE_ADMIN, 'Администратор'),
    )

    username = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя',
        unique=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$')]
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='email',
        unique=True
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='имя',
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='фамилия',
        blank=True
    )
    bio = models.TextField(
        verbose_name='биография',
        blank=True
    )
    role = models.CharField(
        max_length=max([len(role[0]) for role in ROLES]),
        verbose_name='роль',
        choices=ROLES,
        default=ROLE_USER
    )

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == self.ROLE_USER

    @property
    def is_moderator(self):
        return self.role == self.ROLE_MODERATOR

    @property
    def is_admin(self):
        return (
            self.role == self.ROLE_ADMIN
            or self.is_superuser
        )


class Review(models.Model):
    """Модель отзыва на произведение."""

    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='reviews',
                              verbose_name='произведение')
    text = models.TextField('отзыв')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='reviews',
                               verbose_name='автор')
    score = models.PositiveSmallIntegerField(
        'оценка',
        validators=[
            MinValueValidator(1, message='оценка не может быть меньше 1'),
            MaxValueValidator(10, message='оценка не может быть больше 10')
        ]
    )
    pub_date = models.DateTimeField('дата публикации', auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        constraints = [models.UniqueConstraint(fields=['author', 'title'],
                                               name='unique_review')]
        indexes = [
            models.Index(fields=['pub_date']),
            models.Index(fields=['score']),
        ]
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментария к отзыву."""

    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='отзыв')
    text = models.TextField('комментарий')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='автор')
    pub_date = models.DateTimeField('дата публикации', auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        indexes = [
            models.Index(fields=['author']),
            models.Index(fields=['pub_date']),
        ]
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

    def __str__(self):
        return self.text