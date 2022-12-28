from rest_framework import viewsets

from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleGETSerializer,
    TitleSerializer,
)
from .mixins import CreateListDestroyViewSet
from reviews.models import Category, Genre, Title
from .permissions import (AnonimReadOnly)


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
