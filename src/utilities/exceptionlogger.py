# From http://www.obeythetestinggoat.com/how-to-log-exceptions-to-stderr-in-django.html
import logging

class ExceptionLoggingMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        logging.exception('Exception handling request for ' + request.path)
