from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """ Checks if the user is a moderator """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Мoderator').exists()


class IsOwner(permissions.BasePermission):
    """ Checks if the user is the owner of the object """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    """ Custom permission to allow owners to edit their own profile. """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user
