import logging
from django.utils.deprecation import MiddlewareMixin

_logger = logging.getLogger(__name__)


class LogRestMiddleware(MiddlewareMixin):
    """Middleware to log every request/response.
    Is not triggered when the request/response is managed using the cache
    """

    def _log_request(self, request):
        """Log the request"""
        user = str(getattr(request, 'user', ''))
        method = str(getattr(request, 'method', '')).upper()
        body = str(getattr(request, 'body', ''))
        request_path = str(getattr(request, 'path', ''))
        query_params = str(["%s: %s" % (k, v) for k, v in request.GET.items()])
        query_params = query_params if query_params else ''

        _logger.info("req: (%s) [%s] %s %s %s", user, method, request_path, query_params, body)

    def _log_response(self, request, response):
        """Log the response using values from the request"""
        user = str(getattr(request, 'user', ''))
        method = str(getattr(request, 'method', '')).upper()
        content = str(getattr(response, 'content', ''))
        status_code = str(getattr(response, 'status_code', ''))
        status_text = str(getattr(response, 'status_text', ''))
        request_path = str(getattr(request, 'path', ''))
        size = 0
        if hasattr(response, "content"):
            size = str(len(response.content))

        _logger.info("res: (%s) [%s] %s - %s (%s / %s) - %s", user, method, request_path, status_code, status_text,
                      size, content)

    def process_response(self, request, response):
        """Method call when the middleware is used in the `MIDDLEWARE_CLASSES` option in the settings. Django < 1.10"""
        self._log_request(request)
        self._log_response(request, response)
        return response

    def __call__(self, request):
        """Method call when the middleware is used in the `MIDDLEWARE` option in the settings (Django >= 1.10)"""
        self._log_request(request)
        response = self.get_response(request)
        self._log_response(request, response)
        return response
