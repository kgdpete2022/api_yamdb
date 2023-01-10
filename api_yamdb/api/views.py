from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleGETSerializer,
    TitleSerializer,
    UserRegSerializer, 
    UserSerializer,
    UserTokenSerializer
)
from .mixins import CreateListDestroyViewSet
from reviews.models import Category, Genre, Title
from .permissions import (AnonimReadOnly, IsAdminPermission)


class CategoryViewSet(CreateListDestroyViewSet):
    """Вьюсет для создания обьектов класса Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyViewSet):
    """Вьюсет для создания обьектов класса Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для создания обьектов класса Title."""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (AnonimReadOnly)

    def get_serializer_class(self):
        """Определяет какой сериализатор будет использоваться
        для разных типов запроса."""
        if self.request.method == 'GET':
            return TitleGETSerializer
        return TitleSerializer


class CommentsViewSet(viewsets.ModelViewSet):
    pass


class ReviewViewSet(viewsets.ModelViewSet):
    pass


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminPermission]
    lookup_field = 'username'
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == "PATCH":
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role, partial=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def registration(request):
    """Создание пользователя в БД на основе полученных данных и
    отправка кода подтверждения на почту. """
    serializer = UserRegSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.data.get('username')
    email = serializer.data.get('email')
    user, _ = User.objects.get_or_create(email=email, username=username)
    confirmation_code = default_token_generator.make_token(user)

    mail = (
        'Подтверждение регистрации',
        f'Ваше имя пользователя: {user.username} \n'
        f'Ваш код подтверждения: {confirmation_code}',
        'from@example.com',
        [user.email, ]
    )
    send_mail(*mail, fail_silently=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def check_code_and_create_token(request):
    serializer = UserTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.initial_data.get('username')
    confirmation_code = serializer.initial_data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        jwt_token = AccessToken.for_user(user)
        return Response({'token': str(jwt_token)}, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)