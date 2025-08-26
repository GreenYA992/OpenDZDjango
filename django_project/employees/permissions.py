# noinspection PyUnresolvedReferences
from rest_framework import permissions
from django.contrib.auth.models import Group


class IsVisitor(permissions.BasePermission):
    """Права посетителя - только просмотр списка"""
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated and
                request.user.groups.filter(name='Посетитель').exists())

    def has_object_permission(self, request, view, obj):
        # Посетитель может только просматривать список, но не детали
        return view.action == 'list'

class IsViewer(permissions.BasePermission):
    """Права смотрителя"""
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated and
                (request.user.groups.filter(name='Смотритель').exists() or
                 request.user.is_staff))

    def has_object_permission(self, request, view, obj):
        # Смотритель может просматривать все
        return request.method in permissions.SAFE_METHODS

class IsAdmin(permissions.BasePermission):
    """Права администратора"""
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated and
                request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_authenticated and request.user.is_staff