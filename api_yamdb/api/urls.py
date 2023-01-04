from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentsViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet,
                    check_code_and_create_token, registration)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet)
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comment',
)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', registration, name='reg'),
    path('v1/auth/token/', check_code_and_create_token, name='token'),
]
