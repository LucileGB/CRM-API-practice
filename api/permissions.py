import logging

from rest_framework import permissions

logger = logging.getLogger(__name__)


class IsForbidden(permissions.BasePermission):
    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False


class SalesPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            if request.method in permissions.SAFE_METHODS or request.user.is_staff:
                return True

            elif request.user.role == "sa" and request.method != "DELETE":
                return True

            else:
                return False

        except Exception as e:
            logger.warning(e)
            return False

    def has_object_permission(self, request, view, obj):
        try:
            if request.method in permissions.SAFE_METHODS or request.user.is_staff:
                return True

            elif request.user.role == "sa" and request.method == "POST":
                return True

            elif obj.sales_contact.id == request.user.id and request.method != "DELETE":
                return True

            return False

        except Exception as e:
            logger.warning(e)
            return False


class EventPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            if request.method in permissions.SAFE_METHODS or request.user.is_staff:
                return True

            elif request.user.role in ["sa", "su"] and request.method != "DELETE":
                return True

            return False

        except Exception as e:
            logger.warning(e)
            return False

    def has_object_permission(self, request, view, obj):
        try:
            if request.method in permissions.SAFE_METHODS or request.user.is_staff:
                return True

            elif obj.support_contact.id == request.user.id and request.method != "DELETE":
                return True

            elif obj.client.sales_contact.id == request.user.id and request.method != "DELETE":
                return True

            return False

        except Exception as e:
            logger.warning(e)
            return False
