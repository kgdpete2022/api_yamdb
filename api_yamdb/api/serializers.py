import re

from rest_framework import serializers

from reviews.models import User


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
