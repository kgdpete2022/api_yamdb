import re

from django.db.models import Q

from rest_framework import serializers

from reviews.models import Category, Comments, Genre, Review, Title, User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['name', 'slug']
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ['name', 'slug']


class TitleCustomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = [
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        ]


class TitlePostSerializer(TitleCustomSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    rating = serializers.IntegerField(required=False)

    class Meta(TitleCustomSerializer.Meta):
        pass


class TitleGetSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta(TitleCustomSerializer.Meta):
        pass


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        ]


class UserRegSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(max_length=254, required=True)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Недопустимое имя пользователя')
        if not re.fullmatch(r'^[\w.@+-]+', value):
            raise serializers.ValidationError('Неверное значения поля')
        return value

    def validate(self, data):
        email_username_taken = User.objects.filter(
            Q(email=data.get('email')) | Q(username=data.get('username'))
        ).exists()
        user_exists = User.objects.filter(
            email=data.get('email'),
            username=data.get('username')).exists()

        if email_username_taken and not user_exists:
            raise serializers.ValidationError(
                'Пользователем с таким адресом эл. почты'
                'и именем уже существует,'
                'или неверная пара эл. почта / имя пользователя'
            )
        return data


class UserTokenSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ['username', 'confirmation_code']


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = [
            'id',
            'text',
            'author',
            'score',
            'pub_date'
        ]

    def validate(self, data):
        request = self.context['request']
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if not request.method == 'POST':
            return data
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Пользователь может оставить только'
                'один отзыв на произведение'
            )
        return data


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comments
        fields = [
            'id',
            'text',
            'author',
            'pub_date'
        ]
