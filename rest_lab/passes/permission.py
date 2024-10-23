from rest_framework import permissions
from django.contrib.auth.models import User
from .redis import session_storage
from rest_framework import authentication
from rest_framework import exceptions

class IsAuth(permissions.BasePermission):
    def has_permission(self, request, view):
        session_id = request.COOKIES.get("session_id")
        if session_id is None:
            return False
        try:
            username = session_storage.get(session_id).decode("utf-8")
            User.objects.get(username=username)
        except:
            return False
        return True


class IsManagerAuth(permissions.BasePermission):
    def has_permission(self, request, view):
        session_id = request.COOKIES.get("session_id")
        print("MODERATOR")
        if session_id is None:
            return False
        try:
            username = session_storage.get(session_id).decode("utf-8")
        except Exception as e:
            return False
        user = User.objects.get(username=username)
        if user is None:
            return False
        return user.is_staff or user.is_superuser


class IsAdminAuth(permissions.BasePermission):
    def has_permission(self, request, view):
        session_id = request.COOKIES.get("session_id")
        print("COOKIE ADMIN", session_id)
        if session_id is None:
            return False
        try:
            username = session_storage.get(session_id).decode("utf-8")
        except Exception as e:
            return False
        user = User.objects.get(username=username)
        if user is None:
            return False
        return user.is_superuser