from django.conf import settings
from rest_framework import permissions
from meetings.models import User


class MaintainerPermission(permissions.IsAuthenticated):
    """Maintainer权限"""
    message = '需要Maintainer权限！！！'
    level = 2

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if not request.user.level:
            return False
        if request.user.level >= self.level:
            if User.objects.get(id=request.user.id, level=request.user.level):
                return True
            else:
                return False
        else:
            return False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class SponsorPermission(permissions.IsAuthenticated):
    """活动发起人权限"""
    message = '需要活动发起人权限'
    activity_level = 2

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if not request.user.activity_level:
            return False
        if request.user.activity_level >= self.activity_level:
            if User.objects.get(id=request.user.id, activity_level=request.user.activity_level):
                return True
            else:
                return False
        else:
            return False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class AdminPermission(MaintainerPermission):
    """管理员权限"""
    message = '需要管理员权限！！！'
    level = 3


class ActivityAdminPermission(SponsorPermission):
    """活动管理员权限"""
    message = '需要活动管理员权限！！！'
    activity_level = 3


class QueryPermission(permissions.BasePermission):
    """查询权限"""

    def has_permission(self, request, view):
        token = request.GET.get('token')
        if token and token == settings.DEFAULT_CONF.get('QUERY_TOKEN'):
            return True
        else:
            return False

