from django.utils.deprecation import MiddlewareMixin

from app import settings
class DisableCSRFMiddleware(MiddlewareMixin):
   def process_request(self, request):
      if settings.DEBUG:
         setattr(request, '_dont_enforce_csrf_checks', True)