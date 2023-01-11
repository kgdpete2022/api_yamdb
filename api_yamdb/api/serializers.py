import re

from rest_framework import serializers

from reviews.models import Category, Genre, Title, User, Review, Comment


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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')


class UserRegSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(max_length=254, required=True)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Недопустимое имя пользователя')
        if not re.fullmatch(r'^[\w.@+-]+', value):
            raise serializers.ValidationError('Некорректное значения поля')
        return value

    def validate(self, data):
        """Если юзернейм занят, а пользователя
         с такой почтой -  нет - ошибка.
         Если юзернейм занят, и пользователь с
         такими данными есть - разрешить высылку повторного кода
         """
        email_taken = User.objects.filter(
            email=data.get('email')).exists()
        username_taken = User.objects.filter(
            username=data.get('username')).exists()
        user_exists = User.objects.filter(
            email=data.get('email'),
            username=data.get('username')).exists()

        if (email_taken or username_taken) and not user_exists:
            raise serializers.ValidationError(
                'Запрос содержит email или username'
                'зарегистрированного пользователя,'
                'либо данные принадлежат разным пользователям'
            )
        return data


class UserTokenSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""

    author = serializers.SlugRelatedField(many=False, read_only=True,
                                          slug_field='username')
    title = serializers.SlugRelatedField(many=False, read_only=True,
                                         slug_field='id')

    def validate(self, data):
        """Проверка review на уникальность"""

        review = Review.objects.filter(
            title=self.context['view'].kwargs.get('title_id'),
            author=self.context['request'].user
        )
        if review.exists() and self.context['request'].method == 'POST':
            raise serializers.ValidationError('Такой отзыв уже существует.')
        return data

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.SlugRelatedField(many=False, read_only=True,
                                          slug_field='username')
    review = serializers.SlugRelatedField(many=False, read_only=True,
                                          slug_field='score')

    class Meta:
        model = Comment
        fields = '__all__'
