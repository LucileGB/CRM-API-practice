from rest_framework import permissions


class IsForbidden(permissions.BasePermission):
    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False


class IsSales(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            if request.method in permissions.SAFE_METHODS or request.user.is_staff:
                return True

            elif request.user.role == "sa" and request.method == "POST":
                return True

            else:
                return False

        except Exception as e:
            return False

    def has_object_permission(self, request, view, obj):
        try:
            if request.method in permissions.SAFE_METHODS or request.user.is_staff:
                return True
            elif request.user.role == "sa"  and request.method == "PUT":
                return True

            return False
        except Exception as e:
            return False

class EventPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            if request.method in permissions.SAFE_METHODS or request.user.is_staff:
                return True

            elif request.user.role == "sa" and request.method == "POST":
                return True

            elif request.user.role in ["su", "sa"] and request.method == "PUT":
                return True

            return False

        except Exception as e:
            return False

    def has_object_permission(self, request, view, obj):
        try:
            if request.method in permissions.SAFE_METHODS or request.user.is_staff:
                return True

            elif request.user.role in ["su", "sa"] and request.method == "PUT":
                return True

            return False

        except Exception as e:
            return False
