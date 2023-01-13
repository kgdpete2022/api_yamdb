from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Category, Comments, Genre, Review, Title, User


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        ]


@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    resource_classes = [UserResource]
    list_display = [
        'username',
        'email',
        'role',
        'bio',
        'first_name',
        'last_name',
    ]


class TitleResource(resources.ModelResource):
    class Meta:
        model = Title
        fields = [
            'id',
            'name',
            'year',
            'description',
            'category',
            'genre'
        ]


@admin.register(Title)
class TitleAdmin(ImportExportModelAdmin):
    list_display = [
        'id',
        'name',
        'year',
        'description',
        'category'
    ]
    list_editable = ['category']
    search_fields = ['name']
    list_filter = ['year']


class CategoryResource(resources.ModelResource):
    class Meta:
        Model = Category
        fields = [
            'id',
            'name',
            'slug'
        ]


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ['name', 'slug']


class GenreResource(resources.ModelResource):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'slug']


@admin.register(Genre)
class GenreAdmin(ImportExportModelAdmin):
    list_display = ['name', 'slug']


class CommentResource(resources.ModelResource):
    class Meta:
        model = Comments
        fields = [
            'id',
            'review_id',
            'text',
            'author',
            'pub_date'
        ]


@admin.register(Comments)
class CommentAdmin(ImportExportModelAdmin):
    list_display = [
        'review_id',
        'text',
        'author',
        'pub_date'
    ]


class ReviewResource(resources.ModelResource):
    class Meta:
        model = Review
        fields = [
            'id',
            'title_id',
            'text',
            'author',
            'score',
            'pub_date'
        ]


@admin.register(Review)
class ReviewAdmin(ImportExportModelAdmin):
    list_display = [
        'title_id',
        'text',
        'author',
        'score',
        'pub_date'
    ]
