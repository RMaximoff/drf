from rest_framework.permissions import BasePermission


class IsOwnerOrStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderators').exists() or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.groups.filter(name='moderators').exists() or request.user == obj.owner





