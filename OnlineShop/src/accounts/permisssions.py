from django.core.exceptions import PermissionDenied
from django.shortcuts import render


class IsOwnerMixin(object):
    permission_denied_message = "To continue, you must have Owner permission, call admin for further permission."

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff or request.user.roll != 'Owner':
            raise PermissionDenied(self.permission_denied_message)
        else:
            pass
        return super().dispatch(request, *args, **kwargs)

class IsManagerMixin(object):
    permission_denied_message = "To continue, you must have at least Manager permission, call admin for further permission."

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff or (request.user.roll != 'Manager' and request.user.roll != 'Owner'):
            raise PermissionDenied(self.permission_denied_message)
        else:
            pass
        return super().dispatch(request, *args, **kwargs)

class IsOperatorMixin(object):
    permission_denied_message = "To continue, you must have at least Operator permission, call admin for further permission."

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff or (request.user.roll != 'Manager' and request.user.roll != 'Owner' and request.user.roll != 'Operator'):
            raise PermissionDenied(self.permission_denied_message)
        else:
            pass
        return super().dispatch(request, *args, **kwargs)

class IsStaffMixin(object):
    permission_denied_message = "To continue, you must be staff, call admin for further permission."

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied(self.permission_denied_message)
        else:
            pass
        return super().dispatch(request, *args, **kwargs)
