from rest_framework import serializers

from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        model = Genre
        exclude = ('id',)


class TitleGETSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title при GET запросах."""

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'genre',
            'category'
        )


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title при запросах изменения."""

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        # genre — это список айдишников со связью «многие-ко-многим».
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'genre', 'category')

    def to_choice_serializer(self, title):
        """Определяет какой сериализатор будет использоваться для чтения."""
        serializer = TitleGETSerializer(title)
        return serializer.data
