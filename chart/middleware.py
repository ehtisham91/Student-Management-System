from django.http import HttpResponseRedirect
from django.conf import settings
from re import compile

EXEMPT_URLS = [compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]


# class LoginRequiredMiddleware:
#     def process_request(self, request):
#         assert hasattr(request, 'user')
#         if not request.user.is_authenticated():
#             path = request.path_info.lstrip('/')
#             if not any(m.match(path) for m in EXEMPT_URLS):
#                 return HttpResponseRedirect(settings.LOGIN_URL)

def LoginRequiredMiddleware(get_response):
    def middleware(request):
        response = get_response(request)
        if not request.user.is_authenticated:
            path = request.path_info.lstrip('/')
            if not any(m.match(path) for m in EXEMPT_URLS):
                return HttpResponseRedirect(settings.LOGIN_URL)
        return response
    return middleware