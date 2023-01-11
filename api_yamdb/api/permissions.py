from rest_framework import permissions


class CommentsReviewPermission(permissions.BasePermission):
    """Разрешает удалять/добавлять комментарии и отзывы
    только автору, администраторам и суперпользователям."""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        )


class AdminOrReadOnly(permissions.BasePermission):
    """Разрешает анонимному пользователю только безопасные запросы."""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )


class IsAdminPermission(permissions.BasePermission):
    """Проверяет на наличие прав администратора."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser)
        )


class AnonimReadOnly(permissions.BasePermission):
    """Разрешает анонимному пользователю только безопасные запросы."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
