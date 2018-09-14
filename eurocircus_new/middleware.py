from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from django.http import HttpResponseForbidden

class RestrictStaffToAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "Restrict staff to admin middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE_CLASSES setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the RestrictStaffToAdminMiddleware class.")
        if request.user.is_staff and not request.user.is_admin:
            print(request.path)
            if '/admin/' in request.path:
                msg = u'Staff members cannot access the public site.'
                return HttpResponseForbidden(msg)
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response